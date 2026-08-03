from typing import Any, Union

def freeze(
    mod, preserved_attrs: list[str] | None = None, optimize_numerics: bool = True
):
    r"""Freeze ScriptModule, inline submodules, and attributes as constants.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    Freezing a :class:`ScriptModule` will clone it and attempt to inline the cloned
    module's submodules, parameters, and attributes as constants in the TorchScript IR Graph.
    By default, `forward` will be preserved, as well as attributes & methods specified in
    `preserved_attrs`. Additionally, any attribute that is modified within a preserved
    method will be preserved.

    Freezing currently only accepts ScriptModules that are in eval mode.

    Freezing applies generic optimization that will speed up your model regardless of machine.
    To further optimize using server-specific settings, run `optimize_for_inference` after
    freezing.

    Args:
        mod (:class:`ScriptModule`): a module to be frozen
        preserved_attrs (Optional[List[str]]): a list of attributes to preserve in addition to the forward method.
            Attributes modified in preserved methods will also be preserved.
        optimize_numerics (bool): If ``True``, a set of optimization passes will be run that does not strictly
            preserve numerics. Full details of optimization can be found at `torch.jit.run_frozen_optimizations`.

    Returns:
        Frozen :class:`ScriptModule`.

    Example (Freezing a simple module with a Parameter):

    .. testcode::
        import torch
        class MyModule(torch.nn.Module):
            def __init__(self, N, M):
                super().__init__()
                self.weight = torch.nn.Parameter(torch.rand(N, M))
                self.linear = torch.nn.Linear(N, M)

            def forward(self, input):
                output = self.weight.mm(input)
                output = self.linear(output)
                return output

        scripted_module = torch.jit.script(MyModule(2, 3).eval())
        frozen_module = torch.jit.freeze(scripted_module)
        # parameters have been removed and inlined into the Graph as constants
        assert len(list(frozen_module.named_parameters())) == 0
        # See the compiled graph as Python code
        print(frozen_module.code)

    Example (Freezing a module with preserved attributes)

    .. testcode::
        import torch
        class MyModule2(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.modified_tensor = torch.tensor(10.)
                self.version = 1

            def forward(self, input):
                self.modified_tensor += 1
                return input + self.modified_tensor

        scripted_module = torch.jit.script(MyModule2().eval())
        frozen_module = torch.jit.freeze(scripted_module, preserved_attrs=["version"])
        # we've manually preserved `version`, so it still exists on the frozen module and can be modified
        assert frozen_module.version == 1
        frozen_module.version = 2
        # `modified_tensor` is detected as being mutated in the forward, so freezing preserves
        # it to retain model semantics
        assert frozen_module(torch.tensor(1)) == torch.tensor(12)
        # now that we've run it once, the next result will be incremented by one
        assert frozen_module(torch.tensor(1)) == torch.tensor(13)

    Note:
        Freezing submodule attributes is also supported:
        frozen_module = torch.jit.freeze(scripted_module, preserved_attrs=["submodule.version"])

    Note:
        If you're not sure why an attribute is not being inlined as a constant, you can run
        `dump_alias_db` on frozen_module.forward.graph to see if freezing has detected the
        attribute is being modified.

    Note:
        Because freezing makes weights constants and removes module hierarchy, `to` and other
        nn.Module methods to manipulate device or dtype no longer work. As a workaround,
        You can remap devices by specifying `map_location` in `torch.jit.load`, however
        device-specific logic may have been baked into the model.
    """
    warnings.warn(
        "`torch.jit.freeze` is deprecated. Please use `torch.compile` instead.",
        DeprecationWarning,
    )
    if not isinstance(mod, ScriptModule):
        raise RuntimeError(
            "Freezing expects a ScriptModule as input. "
            "Please use torch.jit.script or torch.jit.trace to script your 'nn.Module'."
        )

    if mod.training:
        raise RuntimeError(
            "Freezing is currently only implemented for modules in eval mode. "
            "Please call .eval() on your module before freezing."
        )

    preserved_attrs = preserved_attrs if preserved_attrs is not None else []

    out = RecursiveScriptModule(torch._C._freeze_module(mod._c, preserved_attrs))
    RecursiveScriptModule._finalize_scriptmodule(out)

    preserved_methods = [x for x in preserved_attrs if mod._c._has_method(x)]
    run_frozen_optimizations(out, optimize_numerics, preserved_methods)

    return out


def freeze(
    dynamo_gm: torch.fx.GraphModule,
    aot_autograd_gm: torch.fx.GraphModule,
    example_inputs: list[torch._subclasses.FakeTensor],
) -> tuple[torch.fx.GraphModule, list[int]]:
    """
    Inlines parameters that are not mutated into constants and optimizes the graph through constant propagation
    and other techniques. If enabled, the function also discards the original parameters of the module for memory efficiency.

    Assumes that this function is run in dynamo tracing post aot_autograd.

    Args:
        dynamo_gm (torch.fx.GraphModule): The Dynamo constructed GraphModule.
        aot_autograd_gm (torch.fx.GraphModule): The aot_autograd constructed GraphModule to be frozen.
        example_inputs (List[torch.Tensor]): A list of example input tensors to be used in the freezing process.

    Returns:
        Tuple[torch.fx.GraphModule, List[int]]: A tuple containing the frozen GraphModule and a list of indices
        of the inputs that were preserved (not turned into constants).
    """
    with enter_freezing():
        return _freeze(dynamo_gm, aot_autograd_gm, example_inputs)


def freeze(d):
    """Freeze container to hashable form
    >>> freeze(1)
    1
    >>> freeze([1, 2])
    (1, 2)
    >>> freeze({1: 2})  # doctest: +SKIP
    frozenset([(1, 2)])
    """
    if isinstance(d, dict):
        return frozenset(map(freeze, d.items()))
    if isinstance(d, set):
        return frozenset(map(freeze, d))
    if isinstance(d, (tuple, list)):
        return tuple(map(freeze, d))
    return d


def freeze(
    requirement: list[str] | None = None,
    local_only: bool = False,
    user_only: bool = False,
    paths: list[str] | None = None,
    isolated: bool = False,
    exclude_editable: bool = False,
    skip: Container[str] = (),
) -> Generator[str, None, None]:
    installations: dict[str, FrozenRequirement] = {}

    dists = get_environment(paths).iter_installed_distributions(
        local_only=local_only,
        skip=(),
        user_only=user_only,
    )
    for dist in dists:
        req = FrozenRequirement.from_dist(dist)
        if exclude_editable and req.editable:
            continue
        installations[req.canonical_name] = req

    if requirement:
        # the options that don't get turned into an InstallRequirement
        # should only be emitted once, even if the same option is in multiple
        # requirements files, so we need to keep track of what has been emitted
        # so that we don't emit it again if it's seen again
        emitted_options: set[str] = set()
        # keep track of which files a requirement is in so that we can
        # give an accurate warning if a requirement appears multiple times.
        req_files: dict[str, list[str]] = collections.defaultdict(list)
        for req_file_path in requirement:
            with open(req_file_path) as req_file:
                for line in req_file:
                    if (
                        not line.strip()
                        or line.strip().startswith("#")
                        or line.startswith(
                            (
                                "-r",
                                "--requirement",
                                "-f",
                                "--find-links",
                                "-i",
                                "--index-url",
                                "--pre",
                                "--trusted-host",
                                "--process-dependency-links",
                                "--extra-index-url",
                                "--use-feature",
                            )
                        )
                    ):
                        line = line.rstrip()
                        if line not in emitted_options:
                            emitted_options.add(line)
                            yield line
                        continue

                    if line.startswith(("-e", "--editable")):
                        if line.startswith("-e"):
                            line = line[2:].strip()
                        else:
                            line = line[len("--editable") :].strip().lstrip("=")
                        line_req = install_req_from_editable(
                            line,
                            isolated=isolated,
                        )
                    else:
                        line_req = install_req_from_line(
                            COMMENT_RE.sub("", line).strip(),
                            isolated=isolated,
                        )

                    if not line_req.name:
                        logger.info(
                            "Skipping line in requirement file [%s] because "
                            "it's not clear what it would install: %s",
                            req_file_path,
                            line.strip(),
                        )
                        logger.info(
                            "  (add #egg=PackageName to the URL to avoid"
                            " this warning)"
                        )
                    else:
                        line_req_canonical_name = canonicalize_name(line_req.name)
                        if line_req_canonical_name not in installations:
                            # either it's not installed, or it is installed
                            # but has been processed already
                            if not req_files[line_req.name]:
                                logger.warning(
                                    "Requirement file [%s] contains %s, but "
                                    "package %r is not installed",
                                    req_file_path,
                                    COMMENT_RE.sub("", line).strip(),
                                    line_req.name,
                                )
                            else:
                                req_files[line_req.name].append(req_file_path)
                        else:
                            yield str(installations[line_req_canonical_name]).rstrip()
                            del installations[line_req_canonical_name]
                            req_files[line_req.name].append(req_file_path)

        # Warn about requirements that were included multiple times (in a
        # single requirements file or in different requirements files).
        for name, files in req_files.items():
            if len(files) > 1:
                logger.warning(
                    "Requirement %s included multiple times [%s]",
                    name,
                    ", ".join(sorted(set(files))),
                )

        yield ("## The following requirements were added by pip freeze:")
    for installation in sorted(installations.values(), key=lambda x: x.name.lower()):
        if installation.canonical_name not in skip:
            yield str(installation).rstrip()


def freeze(mask: Union[bool, base.ArrayTree]) -> base.GradientTransformation:
  """Create a transformation that zeros out gradient updates for `mask=True`.

  This essentially freezes (i.e. holding constant) masked parameters.

  The mask must be static (i.e., not dependent on runtime values or updated
  during training) and can be:

    - a single boolean (or 0-d JAX bool array), causing every parameter to be
      either all-frozen (True) or all-trainable (False), or
    - a PyTree of booleans matching the structure of the parameters, where
      each leaf indicates whether that specific parameter leaf should be
      frozen (True) or left unchanged (False).

  Args:
    mask: A boolean prefix tree mask indicating which parameters to freeze.

  Example:
    >>> import jax.numpy as jnp
    >>> from optax import freeze
    >>> params = {'a': jnp.zeros(1), 'b': jnp.zeros(2)}
    >>> mask = {'a': True, 'b': False} # Freeze 'a', train 'b'
    >>> freezer = freeze(mask)

  Returns:
    An Optax `GradientTransformation` which applies `set_to_zero()` wherever
    `mask==True`, and leaves other gradients intact.

  .. seealso::
    :func:`optax.selective_transform` : For partitioning updates
    so only un-frozen parameters are optimized.
  """
  return masked(base.set_to_zero(), mask)


def freeze(G):
    """Modify graph to prevent further change by adding or removing
    nodes or edges.

    Node and edge data can still be modified.

    Parameters
    ----------
    G : graph
      A NetworkX graph

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> G = nx.freeze(G)
    >>> try:
    ...     G.add_edge(4, 5)
    ... except nx.NetworkXError as err:
    ...     print(str(err))
    Frozen graph can't be modified

    Notes
    -----
    To "unfreeze" a graph you must make a copy by creating a new graph object:

    >>> graph = nx.path_graph(4)
    >>> frozen_graph = nx.freeze(graph)
    >>> unfrozen_graph = nx.Graph(frozen_graph)
    >>> nx.is_frozen(unfrozen_graph)
    False

    See Also
    --------
    is_frozen
    """
    G.add_node = frozen
    G.add_nodes_from = frozen
    G.remove_node = frozen
    G.remove_nodes_from = frozen
    G.add_edge = frozen
    G.add_edges_from = frozen
    G.add_weighted_edges_from = frozen
    G.remove_edge = frozen
    G.remove_edges_from = frozen
    G.clear = frozen
    G.clear_edges = frozen
    G.frozen = True
    return G


def freeze(val: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FreezeOp(val=val, results=results, loc=loc, ip=ip).result


def freeze(ref: Ref) -> Array:
  """Invalidate a given reference and return its final value.

  For more information about mutable array references, refer to the
  `Ref guide`_.

  Args:
    ref: A :class:`jax.ref.Ref` object.

  Returns:
    A :class:`jax.Array` containing the contents of ``ref``.

  Examples:
    >>> import jax
    >>> ref = jax.new_ref(jax.numpy.arange(5))
    >>> ref[3] = 100
    >>> ref
    Ref([  0,   1,   2, 100,   4], dtype=int32)

    >>> jax.ref.freeze(ref)
    Array([  0,   1,   2, 100,   4], dtype=int32)

  .. _Ref guide: https://docs.jax.dev/en/latest/array_refs.html
  """
  return freeze_p.bind(ref)


def freeze(xs: Mapping[Any, Any]) -> FrozenDict[Any, Any]:
  """Freeze a nested dict.

  Makes a nested ``dict`` immutable by transforming it into ``FrozenDict``.

  Args:
    xs: Dictionary to freeze (a regualr Python dict).
  Returns:
    The frozen dictionary.
  """
  return FrozenDict(xs)

