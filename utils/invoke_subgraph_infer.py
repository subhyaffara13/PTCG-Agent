
def invoke_subgraph_infer(
    subgraph: GraphModule | FunctionalizeCtxWrapper,
    *operands,
):
    """Inference-only entrypoint for invoke_subgraph that auto-generates identifier.

    This is intended for use cases where we are building an inference graph and
    don't need the forward/backward caching that requires a stable identifier.
    The identifier is automatically computed based on the current proxy mode's
    tracer state.

    If no proxy mode is active, the subgraph is called directly.
    """
    from torch.fx.experimental.proxy_tensor import get_proxy_mode

    proxy_mode = get_proxy_mode()
    if proxy_mode is None:
        # No tracing active, just call the subgraph directly
        if getattr(subgraph, "_boxed_call", False):
            return subgraph(list(operands))
        else:
            return subgraph(*operands)

    from torch._dynamo.utils import get_unique_name_wrt

    # How exactly should we allocate names for the HOP invoke_subgraph we
    # are going to put into the graph?  This is a bit tricky.  In the
    # original design of invoke_subgraph, this HOP never shows up in the
    # wild: it is only generated Dynamo, so Dynamo can take sure of
    # ensuring it picks unique names in the context of the particular
    # Dynamo compilation.  However, these invoke_subgraph are different:
    # they live as Dynamo compiled code that can potentially get traced
    # multiple times!  If they get retraced several times in the same
    # trace, deduplication occurs; but if I make_fx a function f once,
    # and then do a separate new trace, there's no relationship between
    # these.  Additionally, we also want the name we put in the graph to
    # be deterministic, and for it to be indifferent to how many
    # unrelated invoke_subgraphs/make_fxs we've done, prior to THIS
    # particular make_fx.
    #
    # To satisfy all of these constraints, it's impossible to preallocate
    # a name before tracing actually goes through us (since those names
    # would have to all be unique even if a subgraph never gets used.)
    # So we allocate the subgraph a fresh name PER proxy mode, and then
    # consistently reuse it if it hits again.
    #
    # Note we do NOT do equality comparison subgraph, since it has
    # reference equality semantics.

    if subgraph in proxy_mode._invoke_subgraph_cache:
        name = proxy_mode._invoke_subgraph_cache[subgraph]
    else:
        name = get_unique_name_wrt(
            "invoke_subgraph",
            proxy_mode._invoke_subgraph_names,
            requires_suffix=True,
        )
        proxy_mode._invoke_subgraph_names.add(name)
        proxy_mode._invoke_subgraph_cache[subgraph] = name

    return invoke_subgraph(subgraph, name, *operands)

