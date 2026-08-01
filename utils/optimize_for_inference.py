
def optimize_for_inference(
    mod: ScriptModule, other_methods: list[str] | None = None
) -> ScriptModule:
    """
    Perform a set of optimization passes to optimize a model for the purposes of inference.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    If the model is not already frozen, optimize_for_inference
    will invoke `torch.jit.freeze` automatically.

    In addition to generic optimizations that should speed up your model regardless
    of environment, prepare for inference will also bake in build specific settings
    such as the presence of CUDNN or MKLDNN, and may in the future make transformations
    which speed things up on one machine but slow things down on another. Accordingly,
    serialization is not implemented following invoking `optimize_for_inference` and
    is not guaranteed.

    This is still in prototype, and may have the potential to slow down your model.
    Primary use cases that have been targeted so far have been vision models on cpu
    and gpu to a lesser extent.

    Example (optimizing a module with Conv->Batchnorm)::

        import torch

        in_channels, out_channels = 3, 32
        conv = torch.nn.Conv2d(
            in_channels, out_channels, kernel_size=3, stride=2, bias=True
        )
        bn = torch.nn.BatchNorm2d(out_channels, eps=0.001)
        mod = torch.nn.Sequential(conv, bn)
        frozen_mod = torch.jit.optimize_for_inference(torch.jit.script(mod.eval()))
        assert "batch_norm" not in str(frozen_mod.graph)
        # if built with MKLDNN, convolution will be run with MKLDNN weights
        assert "MKLDNN" in frozen_mod.graph
    """
    warnings.warn(
        "`torch.jit.optimize_for_inference` is deprecated. Please use `torch.compile` instead.",
        DeprecationWarning,
    )
    if not isinstance(mod, ScriptModule):
        raise RuntimeError(
            "optimize_for_inference expects a ScriptModule as input. "
            "Please use torch.jit.script or torch.jit.trace to script your 'nn.Module'."
        )

    if other_methods is None:
        other_methods = []

    if hasattr(mod, "training"):
        mod = freeze(mod.eval(), preserved_attrs=other_methods)

    torch._C._jit_pass_optimize_for_inference(mod._c, other_methods)

    return mod


def optimize_for_inference(
    model: torch.nn.Module,
    pass_config: dict[str, Any] | None = None,
    tracer: type[fx.Tracer] = fx.Tracer,
) -> torch.nn.Module:
    """
    Performs a set of optimization passes to optimize a model for the
    purposes of inference. Specifically, the passes that are run are:
    1. Conv/BN fusion
    2. Dropout removal
    3. MKL layout optimizations

    The third optimization takes a function `use_mkl_heuristic` that's used
    to determine whether a subgraph should be explicitly run in MKL layout.

    Note: As FX does not currently handle aliasing, this pass currently
    assumes nothing aliases. If that isn't true, use at your own risk.
    """
    default_pass_config = {
        "conv_bn_fuse": True,
        "remove_dropout": True,
        "mkldnn_layout_optimize": {"heuristic": use_mkl_length},
    }
    if pass_config is None:
        pass_config = {}
    default_pass_config.update(pass_config)

    if default_pass_config["conv_bn_fuse"]:
        model = fuse(model)
    if default_pass_config["remove_dropout"]:
        model = remove_dropout(model)
    if default_pass_config["mkldnn_layout_optimize"] is False:
        return model
    if not isinstance(default_pass_config["mkldnn_layout_optimize"], dict):
        raise RuntimeError("mkldnn_layout_optimize config is not a dict")
    if "heuristic" not in default_pass_config["mkldnn_layout_optimize"]:
        raise RuntimeError("Heuristic not found in mkldnn_layout_optimize config")
    use_mkl_heuristic = default_pass_config["mkldnn_layout_optimize"]["heuristic"]

    cur_tracer = tracer()
    fx_graph = cur_tracer.trace(copy.deepcopy(model))
    fx.GraphModule(cur_tracer.root, fx_graph)
    modules: dict[str, nn.Module] = dict(model.named_modules())

    class MklSupport(Enum):
        NO = 1
        YES = 2
        UNKNOWN = 3

    # Inserts to_mkldnn and to_dense around every node we want to be a MKLDNN node.
    # If the op is in `mkldnn_supported` then we always treat it as a MKLDNN node.
    # However, if it's in `mkldnn_supported_unknown`, then we only treat it as
    # a MKLDNN node if its inputs are MKLDNN nodes.
    for node in list(fx_graph.nodes):
        supports_mkldnn = MklSupport.NO
        if node.op == "call_module":
            cur_module = modules[node.target]
            if type(cur_module) in mkldnn_supported:
                supports_mkldnn = MklSupport.YES
                sample_parameter = next(cur_module.parameters(), None)
                if sample_parameter is not None:
                    if sample_parameter.dtype != torch.float:
                        raise AssertionError(
                            "this pass is only for torch.float modules"
                        )
                    if sample_parameter.device != torch.device("cpu"):
                        raise AssertionError("this pass is only for CPU modules")
        elif node.op == "call_function":
            if node.target in mkldnn_supported:
                supports_mkldnn = MklSupport.YES
            elif node.target in mkldnn_supported_unknown:
                supports_mkldnn = MklSupport.UNKNOWN

        if supports_mkldnn != MklSupport.NO:
            if supports_mkldnn == MklSupport.UNKNOWN:
                if not any(arg.target == "to_dense" for arg in node.args):
                    continue
            with fx_graph.inserting_before(node):
                mkldnn_args = fx.map_arg(
                    node.args, lambda n: fx_graph.call_method("to_mkldnn", (n,))
                )

            node.args = cast(tuple[fx.node.Argument], mkldnn_args)

            with fx_graph.inserting_after(node):
                dense_x = fx_graph.create_node("call_method", "to_dense", (node,))
                node.replace_all_uses_with(dense_x)
                dense_x.args = (node,)

    # Does pre-conversion of all modules into MKLDNN (when possible)
    old_modules = modules_to_mkldnn(list(fx_graph.nodes), modules)
    fx_graph.old_modules = old_modules  # type: ignore[attr-defined]

    # optimizes all a -> to_dense -> to_mkldnn -> b patterns into a -> b
    for node in fx_graph.nodes:
        if node.op == "call_method" and node.target == "to_dense":
            prv_node = node.args[0]
            users = list(node.users)
            for user in users:
                if user.op == "call_method" and user.target == "to_mkldnn":
                    user.replace_all_uses_with(prv_node)
                    fx_graph.erase_node(user)
            if len(node.users) == 0:
                fx_graph.erase_node(node)

    num_nodes = len(fx_graph.nodes)
    uf = UnionFind(num_nodes)

    def get_color(n):
        if hasattr(n, "color"):  # Current node is part of a MKL subgraph
            return uf.find(n.color)
        if hasattr(n, "start_color"):  # Current node is input to MKL subgraph
            return uf.find(n.start_color)
        return None

    # This code is to find each MKLDNN subgraph. Each MKLDNN subgraph consists
    # of input nodes (which are only `to_mkldnn` calls), output nodes
    # (`to_dense` calls), and intermediate nodes, which are run entirely on
    # MKLDNN layout tensors.
    #
    # Specifically, this code does a flood fill on a directed acyclic graph
    # (DAG), starting from each possible "start node" (i.e: `to_mkldnn` nodes).
    # If every node only had one input, this would be sufficient. However, in
    # the case that a node has multiple inputs coming from different start
    # nodes (i.e. colors), we need to join these 2 colors into 1. That's done
    # using a Disjoint Set Union.
    for cur_idx, node in enumerate(fx_graph.nodes):
        if node.op == "call_method" and node.target == "to_mkldnn":
            node.start_color = cur_idx
            uf.make_set(cur_idx)
        elif node.op == "call_method" and node.target == "to_dense":
            if get_color(node.args[0]) is None:
                raise AssertionError("Expected color for to_dense input")
            node.end_color = get_color(node.args[0])
        else:
            cur_colors = [
                get_color(i)
                for i in node.all_input_nodes
                if isinstance(i, fx.Node)
                if get_color(i) is not None
            ]

            if len(cur_colors) == 0:
                continue
            if any(i is None for i in cur_colors):
                raise AssertionError("Found None in cur_colors")
            cur_colors = sorted(cur_colors)
            node.color = cur_colors[0]
            for other_color in cur_colors[1:]:
                uf.join(cur_colors[0], other_color)

    mkldnn_graphs: dict[int, MklSubgraph] = defaultdict(lambda: MklSubgraph(fx_graph))
    for node in fx_graph.nodes:
        if hasattr(node, "color"):
            mkldnn_graphs[uf.find(node.color)].nodes.append(node)
        if hasattr(node, "start_color"):
            mkldnn_graphs[uf.find(node.start_color)].start_nodes.append(node)
        if hasattr(node, "end_color"):
            mkldnn_graphs[uf.find(node.end_color)].end_nodes.append(node)

    # Now that we have all the subgraphs, we need to decide which MKLDNN
    # subgraphs we actually want to keep in MKLDNN.
    for graph in mkldnn_graphs.values():
        if not use_mkl_heuristic(graph):
            for node in graph.start_nodes + graph.end_nodes:
                prv = node.args[0]
                node.replace_all_uses_with(prv)  # type: ignore[arg-type]
                fx_graph.erase_node(node)
            reset_modules(graph.nodes, modules, old_modules)

    mkldnn_conversions = 0
    for node in fx_graph.nodes:
        if node.target == "to_mkldnn" or node.target == "to_dense":
            mkldnn_conversions += 1

    logging.getLogger(__name__).info("mkldnn conversions: %s", mkldnn_conversions)
    fx_graph.lint()
    result = fx.GraphModule(model, fx_graph)
    return result

