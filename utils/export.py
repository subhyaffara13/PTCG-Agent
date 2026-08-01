
def export(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    This decorator indicates that a method on an ``nn.Module`` is used as an entry point into a
    :class:`ScriptModule` and should be compiled.

    .. deprecated:: 2.5
        Please use :func:`torch.compile` instead.

    ``forward`` implicitly is assumed to be an entry point, so it does not need this decorator.
    Functions and methods called from ``forward`` are compiled as they are seen
    by the compiler, so they do not need this decorator either.

    Example (using ``@torch.jit.export`` on a method):

    .. testcode::

        import torch
        import torch.nn as nn

        class MyModule(nn.Module):
            def implicitly_compiled_method(self, x):
                return x + 99

            # `forward` is implicitly decorated with `@torch.jit.export`,
            # so adding it here would have no effect
            def forward(self, x):
                return x + 10

            @torch.jit.export
            def another_forward(self, x):
                # When the compiler sees this call, it will compile
                # `implicitly_compiled_method`
                return self.implicitly_compiled_method(x)

            def unused_method(self, x):
                return x - 20

        # `m` will contain compiled methods:
        #     `forward`
        #     `another_forward`
        #     `implicitly_compiled_method`
        # `unused_method` will not be compiled since it was not called from
        # any compiled methods and wasn't decorated with `@torch.jit.export`
        m = torch.jit.script(MyModule())
    """
    fn._torchscript_modifier = FunctionModifiers.EXPORT  # type:ignore[attr-defined]
    return fn


def export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any] | None = None,
    *,
    dynamic_shapes: dict[str, Any] | tuple[Any, ...] | list[Any] | None = None,
    strict: bool = False,
    preserve_module_call_signature: tuple[str, ...] = (),
    prefer_deferred_runtime_asserts_over_guards: bool = False,
) -> ExportedProgram:
    """
    :func:`export` takes any nn.Module along with example inputs, and produces a traced graph representing
    only the Tensor computation of the function in an Ahead-of-Time (AOT) fashion,
    which can subsequently be executed with different inputs or serialized.  The
    traced graph (1) produces normalized operators in the functional ATen operator set
    (as well as any user-specified custom operators), (2) has eliminated all Python control
    flow and data structures (with certain exceptions), and (3) records the set of
    shape constraints needed to show that this normalization and control-flow elimination
    is sound for future inputs.

    **Soundness Guarantee**

    While tracing, :func:`export()` takes note of shape-related assumptions
    made by the user program and the underlying PyTorch operator kernels.
    The output :class:`ExportedProgram` is considered valid only when these
    assumptions hold true.

    Tracing makes assumptions on the shapes (not values) of input tensors.
    Such assumptions must be validated at graph capture time for :func:`export`
    to succeed. Specifically:

    - Assumptions on static shapes of input tensors are automatically validated without additional effort.
    - Assumptions on dynamic shape of input tensors require explicit specification
      by using the :func:`Dim` API to construct dynamic dimensions and by associating
      them with example inputs through the ``dynamic_shapes`` argument.

    If any assumption can not be validated, a fatal error will be raised. When that happens,
    the error message will include suggested fixes to the specification that are needed
    to validate the assumptions. For example :func:`export` might suggest the
    following fix to the definition of a dynamic dimension ``dim0_x``, say appearing in the
    shape associated with input ``x``, that was previously defined as ``Dim("dim0_x")``::

        dim = Dim("dim0_x", max=5)

    This example means the generated code requires dimension 0 of input ``x`` to be less
    than or equal to 5 to be valid. You can inspect the suggested fixes to dynamic dimension
    definitions and then copy them verbatim into your code without needing to change the
    ``dynamic_shapes`` argument to your :func:`export` call.

    Args:
        mod: We will trace the forward method of this module.

        args: Example positional inputs.

        kwargs: Optional example keyword inputs.

        dynamic_shapes:
         An optional argument where the type should either be:
         1) a dict from argument names of ``f`` to their dynamic shape specifications,
         2) a tuple that specifies dynamic shape specifications for each input in original order.
         If you are specifying dynamism on keyword args, you will need to pass them in the order that
         is defined in the original function signature.

         The dynamic shape of a tensor argument can be specified as either
         (1) a dict from dynamic dimension indices to :func:`Dim` types, where it is
         not required to include static dimension indices in this dict, but when they are,
         they should be mapped to None; or (2) a tuple / list of :func:`Dim` types or None,
         where the :func:`Dim` types correspond to dynamic dimensions, and static dimensions
         are denoted by None. Arguments that are dicts or tuples / lists of tensors are
         recursively specified by using mappings or sequences of contained specifications.

        strict: When disabled (default), the export function will trace the program through
         Python runtime, which by itself will not validate some of the implicit assumptions
         baked into the graph. It will still validate most critical assumptions like shape
         safety. When enabled (by setting ``strict=True``), the export function will trace
         the program through TorchDynamo which will ensure the soundness of the resulting
         graph. TorchDynamo has limited Python feature coverage, thus you may experience more
         errors. Note that toggling this argument does not affect the resulting IR spec to be
         different and the model will be serialized in the same way regardless of what value
         is passed here.

        preserve_module_call_signature: A list of submodule paths for which the original
         calling conventions are preserved as metadata. The metadata will be used when calling
         torch.export.unflatten to preserve the original calling conventions of modules.

    Returns:
        An :class:`ExportedProgram` containing the traced callable.

    **Acceptable input/output types**

    Acceptable types of inputs (for ``args`` and ``kwargs``) and outputs include:

    - Primitive types, i.e. ``torch.Tensor``, ``int``, ``float``, ``bool`` and ``str``.
    - Dataclasses, but they must be registered by calling :func:`register_dataclass` first.
    - (Nested) Data structures comprising of ``dict``, ``list``, ``tuple``, ``namedtuple`` and
      ``OrderedDict`` containing all above types.

    """
    from ._trace import _export

    if not isinstance(mod, torch.nn.Module):
        raise ValueError(
            f"Expected `mod` to be an instance of `torch.nn.Module`, got {type(mod)}."
        )
    if isinstance(mod, torch.jit.ScriptModule):
        raise ValueError(
            "Exporting a ScriptModule is not supported. "
            "Maybe try converting your ScriptModule to an ExportedProgram "
            "using `TS2EPConverter(mod, args, kwargs).convert()` instead."
        )

    try:
        return _export(
            mod,
            args,
            kwargs,
            dynamic_shapes,
            strict=strict,
            preserve_module_call_signature=preserve_module_call_signature,
            pre_dispatch=True,
            prefer_deferred_runtime_asserts_over_guards=prefer_deferred_runtime_asserts_over_guards,
        )
    except Exception as e:
        draft_export_msg = (
            "The error above occurred when calling torch.export.export. If you would "
            "like to view some more information about this error, and get a list "
            "of all other errors that may occur in your export call, you can "
            "replace your `export()` call with `draft_export()`."
        )

        # For errors that we know can be caught by draft-export, add the message
        # to ask users to try out draft-export
        if isinstance(
            e,
            (
                torch.fx.experimental.symbolic_shapes.GuardOnDataDependentSymNode,
                torch._subclasses.fake_tensor.UnsupportedOperatorException,
                torch._dynamo.exc.UserError,
                torch.fx.experimental.symbolic_shapes.ConstraintViolationError,
            ),
        ):
            new_msg = str(e) + "\n\n" + draft_export_msg
            e.args = (new_msg,)
        elif isinstance(e, RuntimeError) and "no fake impl registered" in str(e):
            new_msg = str(e) + "\n\n" + draft_export_msg
            e.args = (new_msg,)
        raise e


def export(
    model: torch.nn.Module
    | torch.export.ExportedProgram
    | torch.jit.ScriptModule
    | torch.jit.ScriptFunction,
    args: tuple[Any, ...] = (),
    f: str | os.PathLike | None = None,
    *,
    kwargs: dict[str, Any] | None = None,
    verbose: bool | None = None,
    input_names: Sequence[str] | None = None,
    output_names: Sequence[str] | None = None,
    opset_version: int | None = None,
    dynamo: bool = True,
    # Dynamo only options
    external_data: bool = True,
    dynamic_shapes: dict[str, Any] | tuple[Any, ...] | list[Any] | None = None,
    custom_translation_table: dict[Callable, Callable] | None = None,
    report: bool = False,
    optimize: bool = True,
    verify: bool = False,
    profile: bool = False,
    dump_exported_program: bool = False,
    artifacts_dir: str | os.PathLike = ".",
    # BC options
    export_params: bool = True,
    keep_initializers_as_inputs: bool = False,
    dynamic_axes: Mapping[str, Mapping[int, str]]
    | Mapping[str, Sequence[int]]
    | None = None,
    # Deprecated options
    training: _C_onnx.TrainingMode = _C_onnx.TrainingMode.EVAL,
    operator_export_type: _C_onnx.OperatorExportTypes = _C_onnx.OperatorExportTypes.ONNX,
    do_constant_folding: bool = True,
    custom_opsets: Mapping[str, int] | None = None,
    export_modules_as_functions: bool | Collection[type[torch.nn.Module]] = False,
    autograd_inlining: bool = True,
) -> ONNXProgram | None:
    r"""Exports a model into ONNX format.

    Setting ``dynamo=True`` enables the new ONNX export logic
    which is based on :class:`torch.export.ExportedProgram` and a more modern
    set of translation logic. This is the recommended and default way to export models
    to ONNX.

    When ``dynamo=True``:

    The exporter tries the following strategies to get an ExportedProgram for conversion to ONNX.

    #. If the model is already an ExportedProgram, it will be used as-is.
    #. Use :func:`torch.export.export` and set ``strict=False``.
    #. Use :func:`torch.export.export` and set ``strict=True``.

    Args:
        model: The model to be exported.
        args: Example positional inputs. Any non-Tensor arguments will be hard-coded into the
            exported model; any Tensor arguments will become inputs of the exported model,
            in the order they occur in the tuple.
        f: Path to the output ONNX model file. E.g. "model.onnx". This argument is kept for
            backward compatibility. It is recommended to leave unspecified (None)
            and use the returned :class:`torch.onnx.ONNXProgram` to serialize the model
            to a file instead.
        kwargs: Optional example keyword inputs.
        verbose: Whether to enable verbose logging.
        input_names: names to assign to the input nodes of the graph, in order.
        output_names: names to assign to the output nodes of the graph, in order.
        opset_version: The version of the
            `default (ai.onnx) opset <https://github.com/onnx/onnx/blob/master/docs/Operators.md>`_
            to target. You should set ``opset_version`` according to the supported opset versions
            of the runtime backend or compiler you want to run the exported model with.
            Leave as default (``None``) to use the recommended version, or refer to
            the ONNX operators documentation for more information.
        dynamo: Whether to export the model with ``torch.export`` ExportedProgram instead of TorchScript.
        external_data: Whether to save the model weights as an external data file.
            This is required for models with large weights that exceed the ONNX file size limit (2GB).
            When False, the weights are saved in the ONNX file with the model architecture.
        dynamic_shapes: A dictionary or a tuple of dynamic shapes for the model inputs. Refer to
            :func:`torch.export.export` for more details. This is only used (and preferred) when dynamo is True.
            Note that dynamic_shapes is designed to be used when the model is exported with dynamo=True, while
            dynamic_axes is used when dynamo=False.
        custom_translation_table: A dictionary of custom decompositions for operators in the model.
            The dictionary should have the callable target in the fx Node as the key (e.g. ``torch.ops.aten.stft.default``),
            and the value should be a function that builds that graph using ONNX Script. This option
            is only valid when dynamo is True.
        report: Whether to generate a markdown report for the export process. This option
            is only valid when dynamo is True.
        optimize: Whether to optimize the exported model. This option
            is only valid when dynamo is True. Default is True.
        verify: Whether to verify the exported model using ONNX Runtime. This option
            is only valid when dynamo is True.
        profile: Whether to profile the export process. This option
            is only valid when dynamo is True.
        dump_exported_program: Whether to dump the :class:`torch.export.ExportedProgram` to a file.
            This is useful for debugging the exporter. This option is only valid when dynamo is True.
        artifacts_dir: The directory to save the debugging artifacts like the report and the serialized
            exported program. This option is only valid when dynamo is True.
        export_params: **When ``f`` is specified**: If false, parameters (weights) will not be exported.

            You can also leave it unspecified and use the returned :class:`torch.onnx.ONNXProgram`
            to control how initializers are treated when serializing the model.
        keep_initializers_as_inputs: **When ``f`` is specified**: If True, all the
            initializers (typically corresponding to model weights) in the
            exported graph will also be added as inputs to the graph. If False,
            then initializers are not added as inputs to the graph, and only
            the user inputs are added as inputs.

            Set this to True if you intend to supply model weights at runtime.
            Set it to False if the weights are static to allow for better optimizations
            (e.g. constant folding) by backends/runtimes.

            You can also leave it unspecified and use the returned :class:`torch.onnx.ONNXProgram`
            to control how initializers are treated when serializing the model.
        dynamic_axes:
            Deprecated: Prefer specifying ``dynamic_shapes`` when ``dynamo=True``.

            By default the exported model will have the shapes of all input and output tensors
            set to exactly match those given in ``args``. To specify axes of tensors as
            dynamic (i.e. known only at run-time), set ``dynamic_axes`` to a dict with schema:

            * KEY (str): an input or output name. Each name must also be provided in ``input_names`` or
                ``output_names``.
            * VALUE (dict or list): If a dict, keys are axis indices and values are axis names. If a
                list, each element is an axis index.

            For example::

                class SumModule(torch.nn.Module):
                    def forward(self, x):
                        return torch.sum(x, dim=1)


                torch.onnx.export(
                    SumModule(),
                    (torch.ones(2, 2),),
                    "onnx.pb",
                    input_names=["x"],
                    output_names=["sum"],
                )

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                ...

            While::

                torch.onnx.export(
                    SumModule(),
                    (torch.ones(2, 2),),
                    "onnx.pb",
                    input_names=["x"],
                    output_names=["sum"],
                    dynamic_axes={
                        # dict value: manually named axes
                        "x": {0: "my_custom_axis_name"},
                        # list value: automatic names
                        "sum": [0],
                    },
                )

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_param: "my_custom_axis_name"  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_param: "sum_dynamic_axes_1"  # axis 0
                ...

        training: Deprecated option. Instead, set the training mode of the model before exporting.
        operator_export_type: Deprecated option. Only ONNX is supported.
        do_constant_folding: Deprecated option.
        custom_opsets: Deprecated option.
        export_modules_as_functions: Deprecated option.
        autograd_inlining: Deprecated option.

    Returns:
        :class:`torch.onnx.ONNXProgram` if dynamo is True, otherwise None.

    .. versionchanged:: 2.6
        ``training`` is now deprecated. Instead, set the training mode of the model before exporting.
        ``operator_export_type`` is now deprecated. Only ONNX is supported.
        ``do_constant_folding`` is now deprecated. It is always enabled.
        ``export_modules_as_functions`` is now deprecated.
        ``autograd_inlining`` is now deprecated.
    .. versionchanged:: 2.7
        ``optimize`` is now True by default.
    .. versionchanged:: 2.9
        ``dynamo`` is now True by default.
    .. versionchanged:: 2.11
        ``fallback`` option has been removed.
    """
    if dynamo is True or isinstance(
        model, (torch.export.ExportedProgram, ExportableModule)
    ):
        from torch.onnx._internal.exporter import _compat

        if isinstance(args, torch.Tensor):
            args = (args,)

        return _compat.export_compat(
            model,
            args,
            f,
            kwargs=kwargs,
            export_params=export_params,
            verbose=verbose,
            input_names=input_names,
            output_names=output_names,
            opset_version=opset_version,
            custom_translation_table=custom_translation_table,
            dynamic_axes=dynamic_axes,
            keep_initializers_as_inputs=keep_initializers_as_inputs,
            external_data=external_data,
            dynamic_shapes=dynamic_shapes,
            report=report,
            optimize=optimize,
            verify=verify,
            profile=profile,
            dump_exported_program=dump_exported_program,
            artifacts_dir=artifacts_dir,
        )
    else:
        import warnings

        from ._internal.torchscript_exporter.utils import export

        warnings.warn(
            "You are using the legacy TorchScript-based ONNX export. Starting in PyTorch 2.9, "
            "the new torch.export-based ONNX exporter has become the default. "
            "Learn more about the new export logic: https://docs.pytorch.org/docs/stable/onnx_export.html. "
            "For exporting control flow: "
            "https://pytorch.org/tutorials/beginner/onnx/export_control_flow_model_to_onnx_tutorial.html",
            category=DeprecationWarning,
            stacklevel=2,
        )

        if dynamic_shapes:
            raise ValueError(
                "The exporter only supports dynamic shapes "
                "through parameter dynamic_axes when dynamo=False."
            )

        export(
            model,
            args,
            f,  # type: ignore[arg-type]
            kwargs=kwargs,
            export_params=export_params,
            verbose=verbose is True,
            input_names=input_names,
            output_names=output_names,
            opset_version=opset_version,
            dynamic_axes=dynamic_axes,
            keep_initializers_as_inputs=keep_initializers_as_inputs,
            training=training,
            operator_export_type=operator_export_type,
            do_constant_folding=do_constant_folding,
            custom_opsets=custom_opsets,
            export_modules_as_functions=export_modules_as_functions,
            autograd_inlining=autograd_inlining,
        )
        return None


def export(
    f: Callable[..., Any],
    *extra_args: Any,
    aten_graph: bool = False,
    pre_dispatch: bool = False,
    decomposition_table: dict[torch._ops.OpOverload, Callable[..., Any]] | None = None,
    tracing_mode: str = "symbolic",
    dynamic_shapes: dict[str, Any] | tuple[Any] | list[Any] | None = None,
    specialize_float: bool = True,
    assume_static_by_default: bool = False,
    same_signature: bool = True,
    disable_constraint_solver: bool = False,
    prefer_deferred_runtime_asserts_over_guards: bool = False,
    _log_export_usage: bool = True,
    constraints: list[Constraint] | None = None,
    **extra_kwargs: Any,
) -> Callable[..., ExportResult]:
    """
    Export an input function f to a format that can be executed outside of PyTorch using the FX graph.

    Args:
        f (callable): A PyTorch function to be exported.

        aten_graph (bool): If True, exports a graph with ATen operators.
        If False, exports a graph with Python operators. Default is False.

        pre_dispatch (bool): If True, exports a graph with ATen operators,
        but before any logic in the PyTorch dispatcher has run.
        This can be useful if you want to apply further transformations on a graph before running it
        through autograd, autocast, or any other functionalities that are integrated into the dispatcher.
        This flag is only valid if aten_graph=True is set.
        Default is False.

        decomposition_table (dict): A dictionary that maps operators to their decomposition functions.
        Required if aten_graph or tracing_mode is specified. Default is None.

        tracing_mode (str): If "symbolic", turn on dynamic shapes support. Default is "symbolic".

        dynamic_shapes:
         An optional argument where the type should either be:
         1) a dict from argument names of ``f`` to their dynamic shape specifications,
         2) a tuple that specifies dynamic shape specifications for each input in original order.
         If you are specifying dynamism on keyword args, you will need to pass them in the order that
         is defined in the original function signature.

         The dynamic shape of a tensor argument can be specified as either
         (1) a dict from dynamic dimension indices to :func:`Dim` types, where it is
         not required to include static dimension indices in this dict, but when they are,
         they should be mapped to None; or (2) a tuple / list of :func:`Dim` types or None,
         where the :func:`Dim` types correspond to dynamic dimensions, and static dimensions
         are denoted by None. Arguments that are dicts or tuples / lists of tensors are
         recursively specified by using mappings or sequences of contained specifications.

        same_signature (bool): If True, rewrite the returned graph's signature to be the same as f.

        disable_constraint_solver (bool): Whether the dim constraint solver must be disabled.

    Returns:
        A function that given args and kwargs, returns a tuple of (graph, guards)
        Graph: An FX graph representing the execution of the input PyTorch function with the provided arguments and options.
        Guards: The guards we accumulated during tracing f above

    Raises:
        AssertionError: If decomposition_table is specified without setting aten_graph=True,
        or if graph breaks during tracing in export.

        AssertionError: If Dynamo input and output is not consistent with traced input/output.

    Note - this headerdoc was authored by ChatGPT, with slight modifications by the author.
    """
    if config.debug_force_graph_break_on_leaf_return:
        raise unittest.SkipTest("Cannot force graph break on export")

    if _log_export_usage:
        log_export_usage(event="export.private_api", flags={"_dynamo"})

    # Deal with "local variable referenced before assignment"
    _f = f
    _specialize_float = specialize_float
    _assume_static_by_default = assume_static_by_default
    _constraints = constraints

    def inner(*args: Any, **kwargs: Any) -> ExportResult:
        if not _constraints:
            combined_args = _combine_args(_f, args, kwargs)
            constraints = _process_dynamic_shapes(combined_args, dynamic_shapes)
        else:
            constraints = _constraints

        f = _f
        specialize_float = _specialize_float
        assume_static_by_default = _assume_static_by_default
        check_if_dynamo_supported()
        torch._C._log_api_usage_once("torch._dynamo.export")
        if decomposition_table is not None:
            assert aten_graph, (
                "Specifying a decomposition_table table or tracing mode is illegal without setting aten_graph=True"
            )
        if pre_dispatch:
            assert aten_graph, "pre_dispatch=True can only be used when aten_graph=True"
        f = innermost_fn(f)
        call_to_inspect = f.forward if isinstance(f, torch.nn.Module) else f
        original_signature = inspect.signature(call_to_inspect)  # type: ignore[arg-type]
        graph = None
        out_guards = None
        graph_captured_input = None
        graph_captured_result: tuple[torch.Tensor, ...] | None = None
        fake_mode = None
        result_traced = None

        def guard_export_print(guards: _guards.GuardsSet) -> None:
            nonlocal out_guards
            assert out_guards is None, (
                "whole graph export entails exactly one guard export"
            )
            out_guards = guards

        example_inputs: list[Any] = []

        def dynamo_normalization_capturing_compiler(
            gm: torch.fx.GraphModule, inner_example_inputs: list[Any]
        ) -> Callable[..., Any]:
            nonlocal graph
            assert graph is None, (
                "Tried to emit a second graph during export. Tracing through 'f' must produce a single graph."
            )
            graph = gm

            nonlocal fake_mode, example_inputs
            # NB: do NOT pass inner_example_inputs here, we are detecting the
            # Dynamo allocated fake mode, which should be DISTINCT from a
            # potential outer ambient fake mode which the user provided.
            # example_inputs is always the user specified inputs, so they
            # would have the wrong fake mode attached to them
            fake_mode = _guards.detect_fake_mode()
            example_inputs = inner_example_inputs

            def result_capturing_wrapper(*graph_inputs: Any) -> Any:
                nonlocal graph_captured_result
                nonlocal graph_captured_input

                graph_captured_input = graph_inputs
                assert graph is not None

                named_parameters = dict(graph.named_parameters(remove_duplicate=False))
                named_buffers = dict(graph.named_buffers(remove_duplicate=False))

                ambient_fake_mode = (
                    _guards.detect_fake_mode(graph_inputs)
                    if _guards.detect_fake_mode(graph_inputs) is not None
                    else fake_mode
                )

                # We reran fake tensor propagation, but we didn't do
                # anything with the resulting unbacked SymInts.  Drop them
                # from the pending list.
                # NB: this is wrong if graph_captured_result has
                # data-dependent output size!
                ignore_fresh_unbacked = null_context()
                assert ambient_fake_mode is not None
                if shape_env := ambient_fake_mode.shape_env:
                    ignore_fresh_unbacked = shape_env.ignore_fresh_unbacked_symbols()  # type: ignore[assignment]

                with (
                    ambient_fake_mode,
                    enable_python_dispatcher(),
                    ignore_fresh_unbacked,
                ):
                    params_and_buffers = {
                        **named_parameters,
                        **named_buffers,
                    }
                    fake_params_buffers = {}

                    for name, value in params_and_buffers.items():
                        fake_params_buffers[name] = ambient_fake_mode.from_tensor(
                            value, static_shapes=True
                        )

                    from torch._export.non_strict_utils import (
                        key_path_to_source,
                        KeyPath,
                    )

                    def fakify_with_ambient(
                        path: KeyPath, t: torch.Tensor | _IntWrapper | Any
                    ) -> Any:
                        if isinstance(t, torch.Tensor):
                            # pyrefly: ignore [missing-attribute]
                            return ambient_fake_mode.from_tensor(t, static_shapes=True)
                        elif isinstance(t, _IntWrapper):
                            if (
                                t.dynamism is not None
                                and isinstance(t.dynamism, _DimHint)
                                and t.dynamism.type
                                in (
                                    _DimHintType.DYNAMIC,
                                    _DimHintType.AUTO,
                                )
                            ):  # type: ignore[union-attr]
                                source = key_path_to_source(path)
                                symint = ambient_fake_mode.shape_env.create_unspecified_symint_and_symbol(  # type: ignore[union-attr]
                                    t.val, source, DimDynamic.DYNAMIC
                                )
                                return symint
                            else:
                                return t.val
                        else:
                            return t

                    fake_graph_inputs = pytree.tree_map_with_path(
                        fakify_with_ambient, graph_inputs
                    )
                    graph_captured_result = torch.func.functional_call(
                        graph,
                        fake_params_buffers,  # type: ignore[arg-type]
                        fake_graph_inputs,  # type: ignore[arg-type]
                    )

                return graph_captured_result

            return result_capturing_wrapper

        # Note: This is needed by rewrite_signature. We need to put it before
        # optimize_assert since user program may mutate the inputs.
        flat_args, in_spec = pytree.tree_flatten((args, kwargs))

        remove_from_cache(f)
        constraint_violation_error = None
        if tracing_mode != "symbolic":
            assume_static_by_default = True
        with (
            config.patch(
                specialize_int=True,
                specialize_float=specialize_float,
                assume_static_by_default=assume_static_by_default,
                automatic_dynamic_shapes=False,
                capture_dynamic_output_shape_ops=True,
                capture_scalar_outputs=True,
                constant_fold_autograd_profiler_enabled=True,
                prefer_deferred_runtime_asserts_over_guards=prefer_deferred_runtime_asserts_over_guards,
                # install_free_tensors ensures that params and buffers are still
                # added as graph attributes, and makes Dynamo emits graphs that
                # follow export pytree-able input requirements
                install_free_tensors=config.install_free_tensors_for_export,
            ),
            _compiling_state_context(),
        ):
            opt_f = optimize_assert(
                dynamo_normalization_capturing_compiler,
                hooks=Hooks(
                    guard_export_fn=guard_export_print,
                    guard_fail_fn=None,
                ),
                export=True,
                export_constraints=constraints,
            )(f)
            # TODO(voz): We may have instances of `f` that mutate inputs, we should track sideeffects and reject.
            try:
                result_traced = opt_f(*args, **kwargs)
            except ConstraintViolationError as e:
                constraint_violation_error = e
        remove_from_cache(f)

        if (
            not disable_constraint_solver
            and (shape_env := getattr(fake_mode, "shape_env", None)) is not None
            and (dim_constraints := shape_env.dim_constraints) is not None
            and not isinstance(
                call_to_inspect, (torch._ops.OpOverloadPacket, torch._ops.OpOverload)
            )
            and not trace_rules.check(call_to_inspect)
        ):
            dim_constraints.solve()

            forced_specializations = dim_constraints.forced_specializations()

            msg = dim_constraints.prettify_results(
                original_signature,
                dynamic_shapes,
                constraint_violation_error,
                forced_specializations,
            )
            if constraint_violation_error:
                constraint_violation_error.args = (
                    constraint_violation_error.args[0] + msg,
                )
            else:
                if forced_specializations:
                    constraint_violation_error = ConstraintViolationError(msg)
                else:
                    log.info(
                        "Summary of dimension constraints:%s",
                        msg,
                    )

            # Error if we have any constraints on static values

            for k in shape_env.var_to_range:
                if isinstance(k, sympy.Integer):
                    constraint_violation_error = ConstraintViolationError(
                        f"{''.join(traceback.format_list(shape_env.var_to_stack[k]))}\n"
                        "It appears that you're trying to set a constraint on a "
                        f"value which we evaluated to have a static value of {k}. "
                        'Set TORCH_LOGS="+export" for more information.'
                    )
        if constraint_violation_error:
            raise constraint_violation_error

        if graph is None:
            assert same_signature, (
                "Failed to produce a graph during tracing as no tensor operations were found and same_signature is False."
            )
            # If the module does not contain any tensor computation, we would create a graph with inputs and outputs.
            # To be consistent with the graph traced by dynano, `graph` will have only tensor inputs as placeholders
            # and tensor outputs as output nodes. non-tensor inputs and outputs will be added when rewriting signature.
            # We will also construct the `example_inputs`, `graph_captured_input`, and `graph_captured_result` corresponding
            # to `graph`.
            example_inputs = []
            graph_captured_input = ()
            graph_captured_result = ()
            fake_mode = torch._subclasses.FakeTensorMode(
                shape_env=ShapeEnv(), export=True
            )
            if out_guards is None:
                out_guards = _guards.GuardsSet()
            assert out_guards is not None  # suppress mypy error
            parameter_names = list(original_signature.parameters.keys())
            fx_graph = torch.fx.Graph()
            for i, name in enumerate(parameter_names):
                if torch.is_tensor(flat_args[i]):
                    node = fx_graph.placeholder(name)
                    node.meta["val"] = fake_mode.from_tensor(
                        flat_args[i], static_shapes=True
                    )
                    graph_captured_input = graph_captured_input + (flat_args[i],)
                    example_inputs.append(flat_args[i])
            fx_graph.output(graph_captured_result)
            module = torch.nn.Module()
            graph = torch.fx.GraphModule(module, fx_graph)
            log.info(
                "Failed to capture a graph during tracing as no tensor operations were found.:\n\n%s",
                graph.print_readable(print_output=False, colored=True),
            )
        else:
            assert out_guards is not None, "Failed to produce guards during tracing"
            assert fake_mode is not None

            log.info(
                "Dynamo captured graph:\n\n%s",
                graph.print_readable(print_output=False, colored=True),
            )

            # This check need to happened before aten_graph
            # because placeholder's _source_node attribute is not preserved by make_fx
            if same_signature:
                check_signature_rewritable(graph)

        # NB: This is mostly hitting the cache; Dynamo already converted these
        example_fake_inputs = [
            fake_mode.from_tensor(t) if isinstance(t, torch.Tensor) else t
            for t in example_inputs
        ]

        if aten_graph:
            # Running graph with interpreter is needed for propagating the stack_trace
            def graph_with_interpreter(*args: Any) -> Any:
                with torch.fx.traceback.preserve_node_meta():
                    return torch.fx.Interpreter(graph).run(*args)  # type: ignore[arg-type]

            with unset_fake_temporarily(), enable_python_dispatcher(), fake_mode:
                try:
                    graph = make_fx(
                        graph_with_interpreter,
                        decomposition_table=decomposition_table,
                        tracing_mode="real",
                        _allow_non_fake_inputs=True,
                        pre_dispatch=pre_dispatch,
                        _allow_fake_constant=False,
                    )(*example_fake_inputs)
                except CondOpArgsMismatchError as e:
                    # Wrap the internal error to the user-facing error
                    raise UserError(  # noqa: B904
                        UserErrorType.DYNAMIC_CONTROL_FLOW,
                        str(e),
                        case_name="cond_operands",
                    )

            assert graph is not None
            for node in graph.graph.find_nodes(op="get_attr"):
                if isinstance(getattr(graph, node.target), torch.Tensor):  # type: ignore[arg-type]
                    node.meta["val"] = fake_mode.from_tensor(
                        getattr(graph, node.target),  # type: ignore[arg-type]
                        static_shapes=True,
                    )

        if same_signature:
            flat_args_dynamic_dims = [
                {
                    c.dim
                    for c in (constraints or ())
                    if (
                        c.t_id == id(x)
                        and not isinstance(c, _RelaxedConstraint)
                        and c.constraint_range.vr.lower != c.constraint_range.vr.upper
                    )
                }
                for x in flat_args
            ]
            graph = rewrite_signature(
                original_signature,
                graph,
                fake_mode,
                flat_args,
                in_spec,
                example_fake_inputs,
                graph_captured_input,  # type: ignore[arg-type]
                graph_captured_result,
                result_traced,  # type: ignore[possibly-undefined]
                flat_args_dynamic_dims,
            )
        return ExportResult(graph, out_guards)

    if extra_args or extra_kwargs:
        warnings.warn(
            "export(f, *args, **kwargs) is deprecated, use export(f)(*args, **kwargs) instead.  "
            "If you don't migrate, we may break your export call in the future if your user defined kwargs "
            "conflict with future kwargs added to export(f).",
            FutureWarning,
            stacklevel=2,
        )
        return inner(*extra_args, **extra_kwargs)  # type: ignore[return-value]
    else:
        return inner


def export(
    model: torch.nn.Module
    | torch.export.ExportedProgram
    | torch.fx.GraphModule
    | torch.jit.ScriptModule
    | torch.jit.ScriptFunction,
    args: tuple[Any, ...] = (),
    kwargs: dict[str, Any] | None = None,
    *,
    registry: _registration.ONNXRegistry | None = None,
    dynamic_shapes: dict[str, Any] | tuple[Any, ...] | list[Any] | None = None,
    input_names: Sequence[str] | None = None,
    output_names: Sequence[str] | None = None,
    report: bool = False,
    verify: bool = False,
    profile: bool = False,
    dump_exported_program: bool = False,
    artifacts_dir: str | os.PathLike = ".",
    verbose: bool | None = None,
    optimize: bool = True,
    opset_version: int | None = None,
) -> _onnx_program.ONNXProgram:
    """Export a PyTorch model to ONNXProgram.

    Args:
        model: The model to export. This can be a PyTorch nn.Module or an ExportedProgram.
        args: The arguments to pass to the model.
        kwargs: The keyword arguments to pass to the model.
        registry: The registry of all ONNX decompositions.
        dynamic_shapes: Dynamic shapes in the graph.
        input_names: If provided, rename the inputs.
        output_names: If provided, rename the outputs.
        report: Whether to generate an error report if the export fails.
        verify: Whether to verify the ONNX model after exporting.
        profile: Whether to profile the export process. When report is True,
            the profile result will be saved in the report. Otherwise, the profile
            result will be printed.
        dump_exported_program: Whether to save the exported program to a file.
        artifacts_dir: The directory to save the exported program and error reports.
        verbose: Whether to print verbose messages. If None (default), some messages will be printed.
        optimize: Whether to optimize the exported ONNX graph.
        opset_version: The ONNX opset version to use. If None, use the default opset version
            from the registry.

    Returns:
        The ONNXProgram with the exported IR graph.

    Raises:
        TorchExportError: If the export process fails with torch.export.
        ConversionError: If the ExportedProgram to ONNX translation fails.
    """
    # Set up the error reporting facilities
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    profiler = _maybe_start_profiler(profile)

    # Create the artifacts directory if it does not exist
    artifacts_dir = pathlib.Path(artifacts_dir)
    if report or profile or dump_exported_program:
        artifacts_dir.mkdir(parents=True, exist_ok=True)

    verbose_print = _verbose_printer(verbose)
    export_status = _reporting.ExportStatus()
    failed_results: list[_capture_strategies.Result] = []

    program: torch.export.ExportedProgram | None = None
    capture_strategy: str | None = None
    # Step 1: Export the model with torch.export.export if the model is not already an ExportedProgram
    if isinstance(model, torch.export.ExportedProgram):
        # We know the model is already exported program, so the args, kwargs, and dynamic_shapes
        # are not used.
        program = model
        # torch.export.export has strict default to False
        export_status.torch_export_non_strict = True
    else:
        # Convert an nn.Module to an ExportedProgram
        # Try everything 🐰 (all paths for getting an ExportedProgram)
        result: _capture_strategies.Result | None = None
        for strategy_class in _capture_strategies.CAPTURE_STRATEGIES:
            strategy = strategy_class(  # type: ignore[abstract]
                verbose=verbose is not False,  # Treat None as verbose
                dump=dump_exported_program,
                artifacts_dir=artifacts_dir,
                timestamp=timestamp,
            )
            result = strategy(model, args, kwargs, dynamic_shapes=dynamic_shapes)

            # Record the status
            if strategy_class is _capture_strategies.TorchExportNonStrictStrategy:
                export_status.torch_export_non_strict = result.success
            elif strategy_class is _capture_strategies.TorchExportStrictStrategy:
                export_status.torch_export_strict = result.success
            elif strategy_class is _capture_strategies.TorchExportDraftExportStrategy:
                export_status.torch_export_draft_export = result.success

            if result.exception is not None:
                failed_results.append(result)
            if result.success:
                if result.exported_program is None:
                    raise AssertionError("exported_program must be non-None on success")
                program = result.exported_program
                break

        if result is None:
            raise AssertionError("result must be non-None")
        capture_strategy = result.strategy
        if result.exported_program is None:
            # If all strategies fail, produce an error report and raise the first error
            profile_result = _maybe_stop_profiler_and_get_result(profiler)

            if report:
                report_path = artifacts_dir / _reporting.construct_report_file_name(
                    timestamp, export_status
                )

                try:
                    _reporting.create_torch_export_error_report(
                        report_path,
                        _format_exceptions_for_all_strategies(failed_results),
                        export_status=export_status,
                        profile_result=profile_result,
                    )
                except Exception as e_report:
                    verbose_print(
                        f"Failed to save error report due to an error: {e_report}"
                    )
            else:
                report_path = None

            first_error = failed_results[0].exception
            if first_error is None:
                raise AssertionError("first_error must be non-None")

            # NOTE: We only throw the torch.export (first) exception because we want to
            # focus on the torch.export.export error. Errors from other strategies like
            # torch.jit.trace is due to the fallback and can be confusing to users.
            # We save all errors in the error report.
            raise _errors.TorchExportError(
                _STEP_ONE_ERROR_MESSAGE
                + (
                    f"\nError report has been saved to '{report_path}'."
                    if report
                    else ""
                )
                + _summarize_exception_stack(first_error)
            ) from first_error

    if program is None:
        raise AssertionError("program must be non-None")

    if dump_exported_program:
        verbose_print("Dumping ExportedProgram because `dump_exported_program=True`...")
        program_path = artifacts_dir / f"onnx_export_{timestamp}.pt2"
        try:
            torch.export.save(program, program_path)
        except Exception as e:
            verbose_print(f"Failed to save ExportedProgram due to an error: {e}")
        else:
            verbose_print(f"ExportedProgram has been saved to '{program_path}'.")

    # Step 2: Decompose the exported program and insert type promotion nodes
    verbose_print("Run decompositions...")

    try:
        # Build the ONNX function registry
        if registry is None:
            registry = _registration.ONNXRegistry.from_torchlib()

        # Process the exported program to run decompositions and type promotions etc.
        decomposed_program = _prepare_exported_program_for_export(
            program, registry=registry
        )
    except Exception as e:
        export_status.decomposition = False
        verbose_print("Run decompositions... ❌")
        profile_result = _maybe_stop_profiler_and_get_result(profiler)

        if report:
            report_path = artifacts_dir / _reporting.construct_report_file_name(
                timestamp, export_status
            )

            # Run the analysis to get the error report
            try:
                _reporting.create_onnx_export_report(
                    report_path,
                    f"{_format_exceptions_for_all_strategies(failed_results)}\n\n{_format_exception(e)}",
                    program,
                    export_status=export_status,
                    profile_result=profile_result,
                    registry=registry,
                )
            except Exception:
                logger.exception("Failed to save report due to an error.")
        else:
            report_path = None

        raise _errors.ConversionError(
            _STEP_TWO_ERROR_MESSAGE
            + (f"\nError report has been saved to '{report_path}'." if report else "")
            + _summarize_exception_stack(e)
        ) from e
    else:
        export_status.decomposition = True
        verbose_print("Run decompositions... ✅")

    # Step 3: Translate the decomposed program to ONNX and produce ONNXProgram
    verbose_print("Translate the graph into ONNX...")
    if report or profile:
        pre_decomp_unique_ops, post_decomp_unique_ops = _analysis.compare_ops(
            program, decomposed_program
        )
    else:
        pre_decomp_unique_ops = None
        post_decomp_unique_ops = None

    try:
        # Convert the exported program to an ONNX model
        onnx_program = _exported_program_to_onnx_program(
            decomposed_program, registry=registry
        )
        # Record the strategy used for getting the exported program for unit test assertions
        onnx_program._capture_strategy = capture_strategy

        export_status.onnx_translation = True
        verbose_print("Translate the graph into ONNX... ✅")
    except Exception as e:
        export_status.onnx_translation = False
        verbose_print("Translate the graph into ONNX... ❌")
        profile_result = _maybe_stop_profiler_and_get_result(profiler)

        if report:
            report_path = artifacts_dir / _reporting.construct_report_file_name(
                timestamp, export_status
            )

            try:
                if pre_decomp_unique_ops is None:
                    raise AssertionError("pre_decomp_unique_ops must be non-None")
                if post_decomp_unique_ops is None:
                    raise AssertionError("post_decomp_unique_ops must be non-None")

                # Run the analysis to get the error report
                _reporting.create_onnx_export_report(
                    report_path,
                    f"{_format_exceptions_for_all_strategies(failed_results)}\n\n{_format_exception(e)}",
                    decomposed_program,
                    decomp_comparison=_reporting.format_decomp_comparison(
                        pre_decomp_unique_ops, post_decomp_unique_ops
                    ),
                    export_status=export_status,
                    profile_result=profile_result,
                    registry=registry,
                )
                verbose_print(f"Export report has been saved to '{report_path}'.")
            except Exception:
                logger.exception("Failed to save report due to an error.")
        else:
            report_path = None

        raise _errors.ConversionError(
            _STEP_THREE_ERROR_MESSAGE
            + (f"\nError report has been saved to '{report_path}'." if report else "")
            + _summarize_exception_stack(e)
        ) from e

    profile_result = _maybe_stop_profiler_and_get_result(profiler)

    if onnx_program.exported_program is None:
        raise AssertionError("exported_program must be non-None")

    # Converter opset version and optimize
    if opset_version is not None:
        onnx_program.model = onnxscript_apis.convert_version(
            onnx_program.model, opset_version
        )

    if optimize:
        verbose_print("Optimize the ONNX graph...")
        onnx_program.optimize()
        verbose_print("Optimize the ONNX graph... ✅")

    # Run the ONNX passes
    if input_names:
        _ir_passes.rename_inputs(onnx_program.model, input_names)
    if output_names:
        _ir_passes.rename_outputs(onnx_program.model, output_names)

    if not verify:
        # Return if verification is not requested
        if report:
            try:
                if pre_decomp_unique_ops is None:
                    raise AssertionError("pre_decomp_unique_ops must be non-None")
                if post_decomp_unique_ops is None:
                    raise AssertionError("post_decomp_unique_ops must be non-None")
                report_path = artifacts_dir / _reporting.construct_report_file_name(
                    timestamp, export_status
                )
                _reporting.create_onnx_export_report(
                    report_path,
                    "No errors"
                    if not failed_results
                    else _format_exceptions_for_all_strategies(failed_results),
                    onnx_program.exported_program,
                    decomp_comparison=_reporting.format_decomp_comparison(
                        pre_decomp_unique_ops, post_decomp_unique_ops
                    ),
                    export_status=export_status,
                    profile_result=profile_result,
                    model=onnx_program.model,
                    registry=registry,
                )
                verbose_print(f"Export report has been saved to '{report_path}'.")
            except Exception:
                logger.exception("Failed to save report due to an error.")
        elif profile and profile_result is not None:
            verbose_print("Profile result:")
            verbose_print(profile_result)
        return onnx_program

    # Step 4: (verify=True) Check the ONNX model with ONNX checker
    try:
        verbose_print("Check the ONNX model...")
        onnxscript_apis.check_model(onnx_program.model)
        export_status.onnx_checker = True
        verbose_print("Check the ONNX model... ✅")
    except Exception as e:
        export_status.onnx_checker = False
        verbose_print("Check the ONNX model... ❌")
        if report:
            try:
                if pre_decomp_unique_ops is None:
                    raise AssertionError("pre_decomp_unique_ops must be non-None")
                if post_decomp_unique_ops is None:
                    raise AssertionError("post_decomp_unique_ops must be non-None")
                report_path = artifacts_dir / _reporting.construct_report_file_name(
                    timestamp, export_status
                )
                _reporting.create_onnx_export_report(
                    report_path,
                    f"{_format_exceptions_for_all_strategies(failed_results)}\n\n{_format_exception(e)}",
                    onnx_program.exported_program,
                    decomp_comparison=_reporting.format_decomp_comparison(
                        pre_decomp_unique_ops, post_decomp_unique_ops
                    ),
                    export_status=export_status,
                    profile_result=profile_result,
                    model=onnx_program.model,
                    registry=registry,
                )
                verbose_print(f"Export report has been saved to '{report_path}'.")
            except Exception:
                logger.exception("Failed to save report due to an error.")
        logger.warning(
            "Conversion successful but the ONNX model fails ONNX checker. "  # noqa: G004
            "Please create an issue "
            f"in the PyTorch GitHub repository against the {_BLUE}*onnx*{_END} component and "
            "attach the full error stack as well as reproduction scripts. ",
            exc_info=e,
        )
        return onnx_program

    # Step 5: (verify=True) Execute the model with ONNX Runtime
    try:
        verbose_print("Execute the model with ONNX Runtime...")
        verification_results = _verification.verify_onnx_program(onnx_program)
        verbose_print("Execute the model with ONNX Runtime... ✅")
        export_status.onnx_runtime = True
        onnx_runtime_error_message = None
    except Exception as e:
        verbose_print("Execute the model with ONNX Runtime... ❌")
        export_status.onnx_runtime = False
        onnx_runtime_error_message = _format_exception(e)
        verification_message = None

    else:
        # Step 6: (verify=True) Validate the output values
        verbose_print("Verify output accuracy...")
        export_status.output_accuracy = True
        for verification_result in verification_results:
            # TODO(justinchuby): The threshold is arbitrary right now
            if verification_result.max_abs_diff >= 5e-3:
                logger.warning(
                    "Output '%s' has a large absolute difference of %f. ",
                    verification_result.name,
                    verification_result.max_abs_diff,
                )
                export_status.output_accuracy = False
            if verification_result.max_rel_diff >= 1e-1:
                logger.warning(
                    "Output '%s' has a large relative difference of %f. ",
                    verification_result.name,
                    verification_result.max_rel_diff,
                )
                export_status.output_accuracy = False
        if export_status.output_accuracy:
            verbose_print("Verify output accuracy... ✅")
        else:
            verbose_print("Verify output accuracy... ❌")
        verification_message = _reporting.format_verification_infos(
            verification_results
        )

    if report:
        try:
            if pre_decomp_unique_ops is None:
                raise AssertionError("pre_decomp_unique_ops must be non-None")
            if post_decomp_unique_ops is None:
                raise AssertionError("post_decomp_unique_ops must be non-None")

            traceback_lines = []
            if failed_results:
                traceback_lines.append(
                    _format_exceptions_for_all_strategies(failed_results)
                )
            if onnx_runtime_error_message:
                traceback_lines.append("# ⚠️ ONNX Runtime error -----------------------")
                traceback_lines.append(onnx_runtime_error_message)
            if not traceback_lines:
                traceback_lines.append("No errors")

            report_path = artifacts_dir / _reporting.construct_report_file_name(
                timestamp, export_status
            )
            _reporting.create_onnx_export_report(
                report_path,
                "\n\n".join(traceback_lines),
                onnx_program.exported_program,
                profile_result=profile_result,
                export_status=export_status,
                decomp_comparison=_reporting.format_decomp_comparison(
                    pre_decomp_unique_ops, post_decomp_unique_ops
                ),
                model=onnx_program.model,
                registry=registry,
                verification_result=verification_message,
            )
            verbose_print(f"Export report has been saved to '{report_path}'.")
        except Exception:
            logger.exception("Failed to save report due to an error.")

    # Release the inference session created during verification
    onnx_program.release()
    return onnx_program


def export(
    model: torch.nn.Module | torch.jit.ScriptModule | torch.jit.ScriptFunction,
    args: tuple[Any, ...] | torch.Tensor,
    f: str,
    *,
    kwargs: dict[str, Any] | None = None,
    export_params: bool = True,
    verbose: bool = False,
    training: _C_onnx.TrainingMode = _C_onnx.TrainingMode.EVAL,
    input_names: Sequence[str] | None = None,
    output_names: Sequence[str] | None = None,
    operator_export_type: _C_onnx.OperatorExportTypes = _C_onnx.OperatorExportTypes.ONNX,
    opset_version: int | None = None,
    do_constant_folding: bool = True,
    dynamic_axes: Mapping[str, Mapping[int, str]]
    | Mapping[str, Sequence[int]]
    | None = None,
    keep_initializers_as_inputs: bool | None = None,
    custom_opsets: Mapping[str, int] | None = None,
    export_modules_as_functions: bool | Collection[type[torch.nn.Module]] = False,
    autograd_inlining: bool = True,
) -> None:
    r"""Exports a model into ONNX format.

    If ``model`` is not a :class:`torch.jit.ScriptModule` nor a
    :class:`torch.jit.ScriptFunction`, this runs
    ``model`` once in order to convert it to a TorchScript graph to be exported
    (the equivalent of :func:`torch.jit.trace`). Thus this has the same limited support
    for dynamic control flow as :func:`torch.jit.trace`.

    Args:
        model: The model to be exported.
        args:

            args can be structured either as:

            1. ONLY A TUPLE OF ARGUMENTS::

                args = (x, y, z)

            The tuple should contain model inputs such that ``model(*args)`` is a valid
            invocation of the model. Any non-Tensor arguments will be hard-coded into the
            exported model; any Tensor arguments will become inputs of the exported model,
            in the order they occur in the tuple.

            2. A TENSOR::

                args = torch.Tensor([1])

            This is equivalent to a 1-ary tuple of that Tensor.

            3. A TUPLE OF ARGUMENTS ENDING WITH A DICTIONARY OF NAMED ARGUMENTS::

                args = (x, {"y": input_y, "z": input_z})

            All but the last element of the tuple will be passed as non-keyword arguments,
            and named arguments will be set from the last element. If a named argument is
            not present in the dictionary, it is assigned the default value, or None if a
            default value is not provided.

            .. warning::
                This behavior will be deprecated in a future release. Please use the
                kwargs argument instead.

            .. note::
                If a dictionary is the last element of the args tuple, it will be
                interpreted as containing named arguments. In order to pass a dict as the
                last non-keyword arg, provide an empty dict as the last element of the args
                tuple. For example, instead of::

                    torch.onnx.export(
                        model,
                        (
                            x,
                            # WRONG: will be interpreted as named arguments
                            {y: z},
                        ),
                        "test.onnx.pb",
                    )

                Write::

                    torch.onnx.export(model, (x, {y: z}, {}), "test.onnx.pb")

        f: Path to the output ONNX model file. E.g. "model.onnx".
        kwargs: Named arguments to the model.
        export_params: If True, all parameters will
            be exported. Set this to False if you want to export an untrained model.
            In this case, the exported model will first take all of its parameters
            as arguments, with the ordering as specified by ``model.state_dict().values()``
        verbose: if True, prints a description of the
            model being exported to stdout. In addition, the final ONNX graph will include the
            field ``doc_string``` from the exported model which mentions the source code locations
            for ``model``. If True, ONNX exporter logging will be turned on.
        training:
            * ``TrainingMode.EVAL``: export the model in inference mode.
            * ``TrainingMode.PRESERVE``: export the model in inference mode if model.training is
                False and in training mode if model.training is True.
            * ``TrainingMode.TRAINING``: export the model in training mode. Disables optimizations
                which might interfere with training.
        input_names (list of str, default empty list): names to assign to the
            input nodes of the graph, in order.
        output_names (list of str, default empty list): names to assign to the
            output nodes of the graph, in order.
        operator_export_type (enum, default OperatorExportTypes.ONNX):

            .. warning::
                This option will be deprecated in a future release. Future exported
                graphs will always use the default opset domain.

            * ``OperatorExportTypes.ONNX``: Export all ops as regular ONNX ops
                (in the default opset domain).
            * ``OperatorExportTypes.ONNX_FALLTHROUGH``: Try to convert all ops
                to standard ONNX ops in the default opset domain. If unable to do so
                (e.g. because support has not been added to convert a particular torch op to ONNX),
                fall back to exporting the op into a custom opset domain without conversion. Applies
                to `custom ops <https://pytorch.org/tutorials/advanced/torch_script_custom_ops.html>`_
                as well as ATen ops. For the exported model to be usable, the runtime must support
                these non-standard ops.
            * ``OperatorExportTypes.ONNX_ATEN``: All ATen ops (in the TorchScript namespace "aten")
                are exported as ATen ops (in opset domain "org.pytorch.aten").
                `ATen <https://pytorch.org/cppdocs/#aten>`_ is PyTorch's built-in tensor library, so
                this instructs the runtime to use PyTorch's implementation of these ops.

                .. warning::

                    Models exported this way are probably runnable only by Caffe2.

                    This may be useful if the numeric differences in implementations of operators are
                    causing large differences in behavior between PyTorch and Caffe2 (which is more
                    common on untrained models).

            * ``OperatorExportTypes.ONNX_ATEN_FALLBACK``: Try to export each ATen op
                (in the TorchScript namespace "aten") as a regular ONNX op. If we are unable to do so
                (e.g. because support has not been added to convert a particular torch op to ONNX),
                fall back to exporting an ATen op. See documentation on OperatorExportTypes.ONNX_ATEN for
                context.
                For example::

                    graph(%0 : Float):
                    %3 : int = prim::Constant[value=0]()
                    # conversion unsupported
                    %4 : Float = aten::triu(%0, %3)
                    # conversion supported
                    %5 : Float = aten::mul(%4, %0)
                    return (%5)

                Assuming ``aten::triu`` is not supported in ONNX, this will be exported as::

                    graph(%0 : Float):
                    %1 : Long() = onnx::Constant[value={0}]()
                    # not converted
                    %2 : Float = aten::ATen[operator="triu"](%0, %1)
                    # converted
                    %3 : Float = onnx::Mul(%2, %0)
                    return (%3)

                .. warning::

                    Models exported this way are probably runnable only by Caffe2.

        opset_version (int, default 18): The version of the
            `default (ai.onnx) opset <https://github.com/onnx/onnx/blob/master/docs/Operators.md>`_
            to target. Must be >= 7.
        do_constant_folding: Apply the constant-folding optimization.
            Constant-folding will replace some of the ops that have all constant inputs
            with pre-computed constant nodes.
        dynamic_axes:

            By default the exported model will have the shapes of all input and output tensors
            set to exactly match those given in ``args``. To specify axes of tensors as
            dynamic (i.e. known only at run-time), set ``dynamic_axes`` to a dict with schema:

            * KEY (str): an input or output name. Each name must also be provided in ``input_names`` or
                ``output_names``.
            * VALUE (dict or list): If a dict, keys are axis indices and values are axis names. If a
                list, each element is an axis index.

            For example::

                class SumModule(torch.nn.Module):
                    def forward(self, x):
                        return torch.sum(x, dim=1)


                torch.onnx.export(
                    SumModule(),
                    (torch.ones(2, 2),),
                    "onnx.pb",
                    input_names=["x"],
                    output_names=["sum"],
                )

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                ...

            While::

                torch.onnx.export(
                    SumModule(),
                    (torch.ones(2, 2),),
                    "onnx.pb",
                    input_names=["x"],
                    output_names=["sum"],
                    dynamic_axes={
                        # dict value: manually named axes
                        "x": {0: "my_custom_axis_name"},
                        # list value: automatic names
                        "sum": [0],
                    },
                )

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_param: "my_custom_axis_name"  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_param: "sum_dynamic_axes_1"  # axis 0
                ...

        keep_initializers_as_inputs: If True, all the
            initializers (typically corresponding to parameters) in the
            exported graph will also be added as inputs to the graph. If False,
            then initializers are not added as inputs to the graph, and only
            the non-parameter inputs are added as inputs.
            This may allow for better optimizations (e.g. constant folding) by
            backends/runtimes.

            If True, `deduplicate_initializers` pass will not be executed. This means
            initializers with duplicated values will not be deduplicated and
            will be treated as distinct inputs to the graph. This allows different
            input initializers to be supplied at the runtime following export.

            If ``opset_version < 9``, initializers MUST be part of graph
            inputs and this argument will be ignored and the behavior will be
            equivalent to setting this argument to True.

        custom_opsets (dict[str, int], default empty dict): A dict with schema:

            * KEY (str): opset domain name
            * VALUE (int): opset version

            If a custom opset is referenced by ``model`` but not mentioned in this dictionary,
            the opset version is set to 1. Only custom opset domain name and version should be
            indicated through this argument.

        export_modules_as_functions: Flag to enable
            exporting all ``nn.Module`` forward calls as local functions in ONNX. Or a set to indicate the
            particular types of modules to export as local functions in ONNX.
            This feature requires ``opset_version`` >= 15, otherwise the export will fail. This is because
            ``opset_version`` < 15 implies IR version < 8, which means no local function support.
            Module variables will be exported as function attributes. There are two categories of function
            attributes.

            1. Annotated attributes: class variables that have type annotations via
            `PEP 526-style <https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations>`_
            will be exported as attributes.
            Annotated attributes are not used inside the subgraph of ONNX local function because
            they are not created by PyTorch JIT tracing, but they may be used by consumers
            to determine whether or not to replace the function with a particular fused kernel.

            2. Inferred attributes: variables that are used by operators inside the module. Attribute names
            will have prefix "inferred::". This is to differentiate from predefined attributes retrieved from
            python module annotations. Inferred attributes are used inside the subgraph of ONNX local function.

            * ``False`` (default): export ``nn.Module`` forward calls as fine grained nodes.
            * ``True``: export all ``nn.Module`` forward calls as local function nodes.
            * Set of type of nn.Module: export ``nn.Module`` forward calls as local function nodes,
                only if the type of the ``nn.Module`` is found in the set.

        autograd_inlining: Flag used to control whether to inline autograd functions.
            Refer to https://github.com/pytorch/pytorch/pull/74765 for more details.

    Raises:
        :class:`torch.onnx.errors.CheckerError`: If the ONNX checker detects an invalid ONNX graph.
        :class:`torch.onnx.errors.UnsupportedOperatorError`: If the ONNX graph cannot be exported because it
            uses an operator that is not supported by the exporter.
        :class:`torch.onnx.errors.OnnxExporterError`: Other errors that can occur during export.
            All errors are subclasses of :class:`errors.OnnxExporterError`.
    """
    if operator_export_type != _C_onnx.OperatorExportTypes.ONNX:
        warnings.warn(
            "Setting `operator_export_type` to something other than default is deprecated. "
            "The option will be removed in a future release.",
            stacklevel=2,
            category=DeprecationWarning,
        )
    if training == _C_onnx.TrainingMode.TRAINING:
        warnings.warn(
            "Setting `training` to something other than default is deprecated. "
            "The option will be removed in a future release. Please set the training mode "
            "before exporting the model.",
            stacklevel=2,
            category=DeprecationWarning,
        )

    args = (args,) if isinstance(args, torch.Tensor) else args
    if kwargs is not None:
        args = args + (kwargs,)

    _export(
        model,
        args,
        f,
        export_params,
        verbose,
        training,
        input_names,
        output_names,
        operator_export_type=operator_export_type,
        opset_version=opset_version,
        do_constant_folding=do_constant_folding,
        dynamic_axes=dynamic_axes,
        keep_initializers_as_inputs=keep_initializers_as_inputs,
        custom_opsets=custom_opsets,
        export_modules_as_functions=export_modules_as_functions,
        autograd_inlining=autograd_inlining,
    )

    return None


def export(
    fun_jit: stages.Wrapped,
    *,
    platforms: Sequence[str] | None = None,
    disabled_checks: Sequence[DisabledSafetyCheck] = (),
    _override_lowering_rules: Sequence[tuple[Any, Any]] | None = None
    ) -> Callable[..., Exported]:
  """Exports a JAX function for persistent serialization.

  Args:
    fun_jit: the function to export. Should be the result of :func:`jax.jit`.
    platforms:
        Optional sequence containing a subset of 'tpu', 'cpu',
        'cuda', 'rocm'. If more than one platform is specified, then
        the exported code takes an argument specifying the platform.
        If None, then use the default JAX backend.
        The calling convention for multiple platforms is explained at
        https://docs.jax.dev/en/latest/export/export.html#module-calling-convention.
    _override_lowering_rules: an optional sequence of custom lowering rules
        for some JAX primitives. Each element of the sequence is a pair
        of a JAX primitive and a lowering function. Defining lowering rules
        is an advanced feature using JAX internal APIs, which are subject
        to change. Furthermore, the responsibility for the stability of the
        MLIR emitted through these custom lowering rules, rests with the user
        of these rules.
    disabled_checks: the safety checks to disable. See documentation for
        of :class:`jax.export.DisabledSafetyCheck`.

  Returns:
    a function that takes args and kwargs pytrees of :class:`jax.ShapeDtypeStruct`,
    or values with ``.shape`` and ``.dtype`` attributes, and returns an
    :class:`~jax.export.Exported`.

  Usage:

      >>> from jax import export
      >>> exported: export.Exported = export.export(jnp.sin)(
      ...     np.arange(4, dtype=np.float32))
      >>>
      >>> # You can inspect the Exported object
      >>> exported.in_avals
      (ShapedArray(float32[4]),)
      >>> blob: bytearray = exported.serialize()
      >>>
      >>> # The serialized bytes are safe to use in a separate process
      >>> rehydrated: export.Exported = export.deserialize(blob)
      >>> rehydrated.fun_name
      'sin'
      >>> rehydrated.call(np.array([.1, .2, .3, .4], dtype=np.float32))
      Array([0.09983342, 0.19866933, 0.29552022, 0.38941833], dtype=float32)
  """
  return _export_internal(fun_jit, platforms=platforms,
                          disabled_checks=disabled_checks,
                          override_lowering_rules=_override_lowering_rules)

