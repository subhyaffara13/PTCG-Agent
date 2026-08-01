
def convert(instance, attrib, new_value):
    """
    Run *attrib*'s converter -- if it has one -- on *new_value* and return the
    result.

    .. versionadded:: 20.1.0
    """
    c = attrib.converter
    if c:
        # This can be removed once we drop 3.8 and use attrs.Converter instead.
        from ._make import Converter

        if not isinstance(c, Converter):
            return c(new_value)

        return c(new_value, instance, attrib)

    return new_value


def convert(nb, to_version):
    """Convert a notebook node object to a specific version.  Assumes that
    all the versions starting from 1 to the latest major X are implemented.
    In other words, there should never be a case where v1 v2 v3 v5 exist without
    a v4.  Also assumes that all conversions can be made in one step increments
    between major versions and ignores minor revisions.

    Parameters
    ----------
    nb : NotebookNode
    to_version : int
        Major revision to convert the notebook to.  Can either be an upgrade or
        a downgrade.

    Raises
    ------
    ValueError
        Notebook failed to convert.
    ValueError
        The version specified is invalid or doesn't exist.
    ValidationError
        Conversion failed due to missing expected attributes.
    """

    # Get input notebook version.
    (version, version_minor) = get_version(nb)

    # Check if destination is target version, if so return contents
    if version == to_version:
        return nb

    # If the version exist, try to convert to it one step at a time.
    if to_version in versions:
        # Get the the version that this recursion will convert to as a step
        # closer to the final revision.  Make sure the newer of the conversion
        # functions is used to perform the conversion.
        if to_version > version:
            step_version = version + 1
            convert_function = versions[step_version].upgrade
        else:
            step_version = version - 1
            convert_function = versions[version].downgrade

        try:
            # Convert and make sure version changed during conversion.
            converted = convert_function(nb)
            if converted.get("nbformat", 1) == version:
                msg = "Failed to convert notebook from v%d to v%d." % (version, step_version)
                raise ValueError(msg)
        except AttributeError as e:
            msg = f"Notebook could not be converted from version {version} to version {step_version} because it's missing a key: {e}"
            raise ValidationError(msg) from None

        # Recursively convert until target version is reached.
        return convert(converted, to_version)
    raise ValueError(
        "Cannot convert notebook to v%d because that version doesn't exist" % (to_version)
    )


def convert(
    module,
    mapping=None,
    inplace=False,
    remove_qconfig=True,
    is_reference=False,
    convert_custom_config_dict=None,
    use_precomputed_fake_quant=False,
):
    r"""Converts submodules in input module to a different module according to `mapping`
    by calling `from_float` method on the target module class. And remove qconfig at the
    end if remove_qconfig is set to True.

    Args:
        `module`: prepared and calibrated module
        `mapping`: a dictionary that maps from source module type to target
                   module type, can be overwritten to allow swapping user defined
                   Modules
        `inplace`: carry out model transformations in-place, the original module
                   is mutated
        `convert_custom_config_dict`: custom configuration dictionary for convert function
        `use_precomputed_fake_quant`: a flag to enable use of precomputed fake quant

    .. code-block:: python

       # Example of convert_custom_config_dict:
       convert_custom_config_dict = {
           # user will manually define the corresponding quantized
           # module class which has a from_observed class method that converts
           # observed custom module to quantized custom module
           "observed_to_quantized_custom_module_class": {
               ObservedCustomModule: QuantizedCustomModule
           }
       }

    """
    torch._C._log_api_usage_once("quantization_api.quantize.convert")
    if not inplace:
        module = copy.deepcopy(module)
    _convert(
        module,
        mapping,
        inplace=True,
        is_reference=is_reference,
        convert_custom_config_dict=convert_custom_config_dict,
        use_precomputed_fake_quant=use_precomputed_fake_quant,
    )
    if remove_qconfig:
        _remove_qconfig(module)
    return module


def convert(
    model: GraphModule,
    is_reference: bool = False,
    convert_custom_config: ConvertCustomConfig | dict[str, Any] | None = None,
    is_standalone_module: bool = False,
    _remove_qconfig_flag: bool = True,
    qconfig_mapping: QConfigMapping | dict[str, Any] | None = None,
    backend_config: BackendConfig | dict[str, Any] | None = None,
    is_decomposed: bool = False,
    keep_original_weights: bool = False,
) -> GraphModule:
    """
    We will convert an observed model (a module with observer calls) to a reference
    quantized model, the rule is simple:
    1. for each observer module call in the graph, we'll convert it to calls to
       quantize and dequantize functions based on the observer instance
    2. for weighted operations like linear/conv, we need to convert them to reference
       quantized module, this requires us to know whether the dtype configured for the
       weight is supported in the backend, this is done in prepare step and the result
       is stored in observed_node_names, we can decide whether we need to swap the
       module based on this set

    Args:
       * `is_standalone_module`: when this flag is True, it means we are quantizing
       a submodule that is not inlined in parent module, and will be quantized
       separately as one unit.

       * `is_decomposed`: a boolean flag to indicate whether we want to use the
        quantize operator for decomposed quantized tensor
        (torch.ops.quantized_decomposed.quantize_per_tensor) or default/standalone
        quantized tensor (torch.quantize_per_tensor)

    Returns:
         a quantized standalone module, whether input/output is quantized is
         specified by prepare_custom_config, with
         input_quantized_idxs, output_quantized_idxs, please
         see docs for :func:`~torch.ao.quantization.prepare_fx` for details
    """
    if convert_custom_config is None:
        convert_custom_config = ConvertCustomConfig()

    if isinstance(convert_custom_config, dict):
        warnings.warn(
            "Passing a convert_custom_config_dict to convert is deprecated and will not be supported "
            "in a future version. Please pass in a ConvertCustomConfig instead.",
            FutureWarning,
            stacklevel=2,
        )
        convert_custom_config = ConvertCustomConfig.from_dict(convert_custom_config)

    if isinstance(qconfig_mapping, dict):
        warnings.warn(
            "Passing a QConfig dictionary to convert is deprecated and will not be supported "
            "in a future version. Please pass in a QConfigMapping instead.",
            FutureWarning,
            stacklevel=2,
        )
        qconfig_mapping = (
            QConfigMapping.from_dict(qconfig_mapping) if qconfig_mapping else None
        )
    qconfig_mapping = copy.deepcopy(qconfig_mapping)
    if not (qconfig_mapping is None or isinstance(qconfig_mapping, QConfigMapping)):
        raise AssertionError("qconfig_mapping must be None or a QConfigMapping")

    if isinstance(backend_config, dict):
        warnings.warn(
            "Passing a backend_config_dict to prepare is deprecated and will not be supported "
            "in a future version. Please pass in a BackendConfig instead.",
            FutureWarning,
            stacklevel=2,
        )
        backend_config = BackendConfig.from_dict(backend_config)

    if backend_config is None:
        backend_config = get_native_backend_config()

    if not _is_observed_module(model):
        raise AssertionError("incoming model must be produced by prepare_fx")
    observed_graph_module_attrs = model.meta["_observed_graph_module_attrs"]
    node_name_to_scope: dict[str, tuple[str, type]] = (
        observed_graph_module_attrs.node_name_to_scope
    )
    prepare_custom_config: PrepareCustomConfig = (
        observed_graph_module_attrs.prepare_custom_config
    )
    observed_node_names: set[str] = observed_graph_module_attrs.observed_node_names
    node_name_to_qconfig: dict[str, QConfigAny] = (
        observed_graph_module_attrs.node_name_to_qconfig
    )  # type: ignore[assignment]

    # mapping from fully qualified module name to module instance
    # for example,
    # {
    #   '': Model(...),
    #   'linear': Linear(...),
    #   'linear.weight_fake_quant': PerChannelMinMaxObserver(...),
    # }
    # We use remove_duplicate=False here because torch.cat uses
    # the same activation_post_process module instance but different names
    modules = dict(model.named_modules(remove_duplicate=False))

    # TODO refactor this code once we update the prepare logic to have additional information on
    # which graph nodes have been observed and share that with convert to decide which observers to ignore.
    if qconfig_mapping:
        prepare_qconfig_mapping: QConfigMapping = (
            observed_graph_module_attrs.qconfig_mapping
        )  # type: ignore[assignment]
        modules_copy = copy.deepcopy(modules)

        if observed_graph_module_attrs.is_qat:
            _update_qconfig_for_qat(qconfig_mapping, backend_config)
        _update_qconfig_for_fusion(model, qconfig_mapping)

        _compare_prepare_convert_qconfig_mappings(
            prepare_qconfig_mapping, qconfig_mapping
        )  # type: ignore[arg-type]
        convert_node_name_to_qconfig = _generate_node_name_to_qconfig(
            model, modules_copy, model.graph, qconfig_mapping, node_name_to_scope
        )
        # check the convert_node_name_to_qconfig generated and ensure that
        # all the values either match what was set in prepare node_name_to_qconfig
        # or are set to None in the convert_node_name_to_qconfig.
        for k, v in node_name_to_qconfig.items():
            if k not in convert_node_name_to_qconfig:
                raise AssertionError(
                    f"Expected key {k} in convert node_name_to_qconfig"
                )
            if convert_node_name_to_qconfig[k] is not None:
                if not qconfig_equals(v, convert_node_name_to_qconfig[k]):
                    raise AssertionError(
                        f"Expected k {k} to have the same value in prepare and convert QConfigMappings, "
                        f"but {v} was updated to {convert_node_name_to_qconfig[k]}"
                    )
        node_name_to_qconfig = convert_node_name_to_qconfig

    custom_module_classes = get_custom_module_class_keys(
        convert_custom_config.observed_to_quantized_mapping
    )
    custom_module_class_mapping = convert_custom_config.observed_to_quantized_mapping

    if observed_graph_module_attrs.equalization_node_name_to_qconfig is not None:
        # If we want to do equalization then do the following:
        # Calculate the equalization scale, update the observers with the scaled
        # inputs, and scale the weight
        weight_eq_obs_dict = update_obs_for_equalization(model, modules)
        convert_eq_obs(model, modules, weight_eq_obs_dict)

    # always run weight observers in the top level forward method
    # for dynamic quant ops or weight only quant ops
    _run_weight_observers(model, backend_config)

    # additional state to override inputs to be quantized, if specified
    # by the user
    placeholder_node_seen_cnt = 0
    input_quantized_idxs: list[int] = prepare_custom_config.input_quantized_indexes
    output_quantized_idxs: list[int] = prepare_custom_config.output_quantized_indexes

    root_module_to_quantized_reference_module = (
        get_root_module_to_quantized_reference_module(backend_config)
    )
    # convert tuples so that it can work with isinstance(module, tuple_of_classes)
    root_module_classes = tuple(root_module_to_quantized_reference_module.keys())
    qat_module_classes = get_qat_module_classes(backend_config)
    fused_module_classes = get_fused_module_classes(backend_config)
    statically_quantized_custom_module_nodes: set[Node] = set()
    model_device = assert_and_get_unique_device(model)

    for node in list(model.graph.nodes):
        if node.op == "placeholder":
            cur_placeholder_node_idx = placeholder_node_seen_cnt
            placeholder_node_seen_cnt += 1
            if cur_placeholder_node_idx in input_quantized_idxs:
                # Inputs are assumed to be quantized if the user specified the
                # input_quantized_idxs override.
                # we need to dequantize the inputs since all operators took
                # floating point inputs in reference quantized models
                _insert_dequantize_node(node, model.graph)
        elif node.op == "output":
            # If the argument is empty we don't need to do anything
            if len(output_quantized_idxs) == 0:
                continue
            # Result are kept quantized if the user specified the
            # output_quantized_idxs override.
            # Remove the dequantize operator for the node in the end if any
            return_node = node
            output = node.args[0]
            # outputs can be Node, list, tuple, dict, other cases are not supported yet
            if isinstance(output, (list, tuple)):  # noqa: UP038
                for idx in output_quantized_idxs:
                    _maybe_recursive_remove_dequantize(
                        output[idx], return_node, model.graph
                    )
            elif isinstance(output, (Node, dict)):  # noqa: UP038
                # we treat dict as a single argument currently, but it can be extended
                # to support {"key": dtype} after we change output_quantized_idxs to
                # dict
                if 0 in output_quantized_idxs:
                    _maybe_recursive_remove_dequantize(output, return_node, model.graph)
            else:
                warnings.warn(
                    f"Unsupported node type for output_quantized_idxs: {type(output)}",
                    stacklevel=2,
                )
        elif node.op == "call_module":
            mod = _get_module(node, modules)
            if mod is None:
                raise AssertionError(
                    "Expected module for call_module node to be present in modules mapping"
                )
            if _is_activation_post_process(mod):
                observed_node = node.args[0]
                if observed_node in statically_quantized_custom_module_nodes:
                    _replace_observer_or_dequant_stub_with_dequantize_node(
                        node, model.graph
                    )
                else:
                    if is_decomposed:
                        _replace_observer_with_quantize_dequantize_node_decomposed(
                            model,
                            node,
                            modules,
                            node_name_to_scope,
                            node_name_to_qconfig,
                            model_device,
                        )
                    else:
                        _replace_observer_with_quantize_dequantize_node(
                            model,
                            node,
                            modules,
                            node_name_to_scope,
                            node_name_to_qconfig,
                            model_device,
                        )
            elif isinstance(mod, DeQuantStub):
                _replace_observer_or_dequant_stub_with_dequantize_node(
                    node, model.graph
                )
            elif _is_observed_standalone_module(mod):
                convert_standalone_module(
                    node, modules, model, is_reference, backend_config
                )
            # below this point `type_before_parametrizations` is used
            # instead of `type` to handle situations with fx quant + sparsity
            elif type_before_parametrizations(mod) in set(root_module_classes).union(
                qat_module_classes
            ).union(fused_module_classes):
                # extra check for fused module classes to make sure they are fused module classes
                # of target modules
                if (
                    type_before_parametrizations(mod) in fused_module_classes
                    and type_before_parametrizations(mod[0]) not in root_module_classes
                ):  # type: ignore[index]
                    continue
                convert_weighted_module(
                    node,
                    modules,
                    observed_node_names,
                    node_name_to_qconfig,
                    backend_config,
                    is_decomposed,
                    is_reference,
                    model_device,
                )
            elif type_before_parametrizations(mod) in custom_module_classes:
                convert_custom_module(
                    node,
                    model.graph,
                    modules,
                    custom_module_class_mapping,
                    statically_quantized_custom_module_nodes,
                )

    # remove deadcode after converting observers to quant/dequant ops
    model.graph.eliminate_dead_code()
    model = GraphModule(model, model.graph)

    # TODO: maybe move this to quantize_fx.py
    if not is_reference:
        model = lower_to_fbgemm(
            model, node_name_to_qconfig, node_name_to_scope, keep_original_weights
        )

    # TODO: this looks hacky, we want to check why we need this and see if we can
    # remove this
    # removes qconfig and activation_post_process modules
    if _remove_qconfig_flag:
        _remove_qconfig(model)
    model.delete_all_unused_submodules()
    model.meta.pop("_observed_graph_module_attrs", None)
    return model


def convert(files: list[str], dest_dir: str, verbose: bool) -> None:
    for pat in files:
        for archive in iglob(pat):
            path = Path(archive)
            if path.suffix == ".egg":
                if path.is_dir():
                    source: ConvertSource = EggDirectorySource(path)
                else:
                    source = EggFileSource(path)
            else:
                source = WininstFileSource(path)

            if verbose:
                print(f"{archive}...", flush=True, end="")

            dest_path = Path(dest_dir) / (
                f"{source.name}-{source.version}-{source.pyver}-{source.abi}"
                f"-{source.platform}.whl"
            )
            with WheelFile(dest_path, "w") as wheelfile:
                for name_or_zinfo, contents in source.generate_contents():
                    wheelfile.writestr(name_or_zinfo, contents)

                # Write the METADATA file
                wheelfile.writestr(
                    f"{source.dist_info_dir}/METADATA",
                    source.metadata.as_string(policy=serialization_policy).encode(
                        "utf-8"
                    ),
                )

                # Write the WHEEL file
                wheel_message = Message()
                wheel_message.add_header("Wheel-Version", "1.0")
                wheel_message.add_header("Generator", GENERATOR)
                wheel_message.add_header(
                    "Root-Is-Purelib", str(source.platform == "any").lower()
                )
                tags = parse_tag(f"{source.pyver}-{source.abi}-{source.platform}")
                for tag in sorted(tags, key=lambda tag: tag.interpreter):
                    wheel_message.add_header("Tag", str(tag))

                wheelfile.writestr(
                    f"{source.dist_info_dir}/WHEEL",
                    wheel_message.as_string(policy=serialization_policy).encode(
                        "utf-8"
                    ),
                )

            if verbose:
                print("OK")


def convert(s, datatype="np.float32"):
    i = int(s, 16)                   # convert from hex to a Python int
    if (datatype == "np.float64"):
        cp = pointer(c_longlong(i))           # make this into a c long long integer
        fp = cast(cp, POINTER(c_double))  # cast the int pointer to a double pointer
    else:
        cp = pointer(c_int(i))           # make this into a c integer
        fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer

    return fp.contents.value         # dereference the pointer, get the float


def convert(graph):
    if isinstance(graph, PlanarEmbedding):
        return LoopbackPlanarEmbedding(graph)
    if isinstance(graph, MultiDiGraph):
        return LoopbackMultiDiGraph(graph)
    if isinstance(graph, MultiGraph):
        return LoopbackMultiGraph(graph)
    if isinstance(graph, DiGraph):
        return LoopbackDiGraph(graph)
    if isinstance(graph, Graph):
        return LoopbackGraph(graph)
    raise TypeError(f"Unsupported type of graph: {type(graph)}")


def convert(filename, cache):
    """
    Convert the named file to png; return the name of the created file.

    If *cache* is True, the result of the conversion is cached in
    `matplotlib.get_cachedir() + '/test_cache/'`.  The caching is based on a
    hash of the exact contents of the input file.  Old cache entries are
    automatically deleted as needed to keep the size of the cache capped to
    twice the size of all baseline images.
    """
    path = Path(filename)
    if not path.exists():
        raise OSError(f"{path} does not exist")
    if path.suffix[1:] not in converter:
        import pytest
        pytest.skip(f"Don't know how to convert {path.suffix} files to png")
    newpath = path.parent / f"{path.stem}_{path.suffix[1:]}.png"

    # Only convert the file if the destination doesn't already exist or
    # is out of date.
    if not newpath.exists() or newpath.stat().st_mtime < path.stat().st_mtime:
        cache_dir = _get_cache_path() if cache else None

        if cache_dir is not None:
            _register_conversion_cache_cleaner_once()
            hash_value = get_file_hash(path)
            cached_path = cache_dir / (hash_value + newpath.suffix)
            if cached_path.exists():
                _log.debug("For %s: reusing cached conversion.", filename)
                shutil.copyfile(cached_path, newpath)
                return str(newpath)

        _log.debug("For %s: converting to png.", filename)
        convert = converter[path.suffix[1:]]
        if path.suffix == ".svg":
            contents = path.read_text(encoding="utf-8")
            # NOTE: This check should be kept in sync with font styling in
            # `lib/matplotlib/backends/backend_svg.py`. If it changes, then be sure to
            # re-generate any SVG test files using this mode, or else such tests will
            # fail to use the converter for the expected images (but will for the
            # results), and the tests will fail strangely.
            if re.search(
                # searches for attributes :
                #   style=[font|font-size|font-weight|
                #          font-family|font-variant|font-style]
                # taking care of the possibility of multiple style attributes
                # before the font styling (i.e. opacity)
                r'style="[^"]*font(|-size|-weight|-family|-variant|-style):',
                contents  # raw contents of the svg file
                    ):
                # for svg.fonttype = none, we explicitly patch the font search
                # path so that fonts shipped by Matplotlib are found.
                convert = _svg_with_matplotlib_fonts_converter
        convert(path, newpath)

        if cache_dir is not None:
            _log.debug("For %s: caching conversion result.", filename)
            shutil.copyfile(newpath, cached_path)

    return str(newpath)


def convert(filenames: Iterable[str]) -> None:
    for filename in filenames:
        convert_file(filename)


def convert(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConvertOp(result=result, operand=operand, loc=loc, ip=ip).result


def convert(dest: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConvertOp(dest=dest, source=source, loc=loc, ip=ip).result


def convert(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConvertOp(result=result, operand=operand, loc=loc, ip=ip).result


def convert(fun_jax: Callable,
            *,
            polymorphic_shapes: str | PolyShape | None | Sequence[str | PolyShape | None] = None,
            polymorphic_constraints: Sequence[str] = (),
            with_gradient: bool = True,
            enable_xla: bool | _DefaultNativeSerialization = DEFAULT_NATIVE_SERIALIZATION,
            native_serialization: bool | _DefaultNativeSerialization = DEFAULT_NATIVE_SERIALIZATION,
            native_serialization_platforms: Sequence[str] | None = None,
            native_serialization_disabled_checks: Sequence[DisabledSafetyCheck] = (),
            ) -> Callable:
  """Allows calling a JAX function from a TensorFlow program.

  See
  [README](https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md)
  for more details about usage and common problems.

  Args:
    fun_jax: target JAX function to be called. Its arguments and return value
      should be JAX arrays, or nested standard Python containers
      (tuple/list/dict) thereof (pytrees).
    polymorphic_shapes: Specifies input shapes to be treated polymorphically
      during lowering.

      .. warning:: The shape-polymorphic lowering is an experimental feature.
        It is meant to be sound, but it is known to reject some JAX programs
        that are shape polymorphic. The details of this feature can change.

      It should be `None` (all arguments are monomorphic), a single PolyShape
      or string (applies to all arguments), or a tuple/list of the same length
      as the function arguments. For each argument the shape specification
      should be `None` (monomorphic argument), or a Python object with the
      same pytree structure as the argument.
      See [how optional parameters are matched to
      arguments](https://docs.jax.dev/en/latest/pytrees.html#applying-optional-parameters-to-pytrees).

      A shape specification for an array argument should be an object
      `PolyShape(dim0, dim1, ..., dimn)`
      where each `dim` is a dimension specification: a positive integer denoting
      a monomorphic dimension of the given size, or a string denoting a
      dimension variable assumed to range over non-zero dimension sizes, or
      the special placeholder string "_" denoting a monomorphic dimension
      whose size is given by the actual argument. As a shortcut, an Ellipsis
      suffix in the list of dimension specifications stands for a list of "_"
      placeholders.

      For convenience, a shape specification can also be given as a string
      representation, e.g.: "batch, ...", "batch, height, width, _", possibly
      with surrounding parentheses: "(batch, ...)".

      The lowering fails if it cannot ensure that the it would produce the same
      sequence of TF ops for any non-zero values of the dimension variables.

      polymorphic_shapes are only supported for positional arguments; shape
      polymorphism is not supported for keyword arguments.

      See [the README](https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#shape-polymorphic-conversion)
      for more details.

    polymorphic_constraints: a sequence of constraints on symbolic dimension
      expressions, of the form `e1 >= e2` or `e1 <= e2`.
      See more details at https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#user-specified-symbolic-constraints.
    with_gradient: if set (default), add a tf.custom_gradient to the lowered
      function, by converting the ``jax.vjp(fun)``. This means that reverse-mode
      TensorFlow AD is supported for the output TensorFlow function, and the
      value of the gradient will be JAX-accurate.
    native_serialization_platforms: Specifies the platform(s)
      for which to lower the code. Must be a tuple of
      strings, including a subset of: 'cpu', 'cuda', 'rocm', 'tpu'.
      The default (`None``), specifies the JAX default
      backend on the machine where the lowering is done.
    native_serialization_disabled_checks: Disables the specified safety checks.
      See docstring of `DisabledSafetyCheck`.

  Returns:
    A version of `fun_jax` that expects TfVals as arguments (or
    tuple/lists/dicts thereof), and returns TfVals as outputs, and uses
    only TensorFlow ops and thus can be called from a TensorFlow program.
  """
  if native_serialization is not DEFAULT_NATIVE_SERIALIZATION:
    warnings.warn(
        "The `native_serialization` parameter is deprecated and "
        "will be removed in a future version of JAX.",
        DeprecationWarning, stacklevel=2)
  del native_serialization
  if enable_xla is not DEFAULT_NATIVE_SERIALIZATION:
    warnings.warn(
        "The `enable_xla` parameter is deprecated and "
        "will be removed in a future version of JAX.",
        DeprecationWarning, stacklevel=2)
  del enable_xla

  if native_serialization_platforms:
    if (not isinstance(native_serialization_platforms, (list, tuple)) or
        not all(p in ["cpu", "cuda", "rocm", "tpu"]
                for p in native_serialization_platforms)):
      raise ValueError(
          "native_serialization_platforms must be a sequence "
          "containing a subset of {'cpu', 'cuda', 'rocm', 'tpu'}. "
          f"Got: {native_serialization_platforms}")
    native_serialization_platforms = tuple(native_serialization_platforms)

  api.check_callable(fun_jax)

  def converted_fun_tf(*args_tf: TfVal, **kwargs_tf: TfVal) -> TfVal:

    # TODO: is there a better way to check if we are inside a transformation?
    if not core.trace_state_clean() and not _thread_local_state.inside_call_tf:
      # It is Ok to nest convert when we are inside a call_tf
      raise ValueError(
          "convert must be used outside all JAX transformations." +
          f"Trace state: {core.trace_ctx}")

    global _has_registered_tf_source_path
    if not _has_registered_tf_source_path:
      source_info_util.register_exclusion(os.path.dirname(tf.__file__))
      _has_registered_tf_source_path = True

    def jax_arg_spec_from_tf(a: TfVal) -> jax.ShapeDtypeStruct:
      # The shape and JAX dtype for a TF argument
      tf_arg_shape = np.shape(a)
      # Fix the shape for TF1
      tf_arg_shape = tuple(d.value
                           if isinstance(d, tf.compat.v1.Dimension) else d
                           for d in tf_arg_shape)
      _, a_jax_dtype = _tfval_to_tensor_jax_dtype(a)
      # We count on the fact that jax.ShapeDtypeStruct allows shapes that
      # contain None.
      return jax.ShapeDtypeStruct(tf_arg_shape, a_jax_dtype)

    args_jax_specs = tree_util.tree_map(jax_arg_spec_from_tf, args_tf)
    args_specs = export.symbolic_args_specs(
        args_jax_specs, polymorphic_shapes,
        constraints=polymorphic_constraints)
    # The polymorphic_shapes argument refers to positional arguments only.
    # We assume None for the kwargs.
    kwargs_jax_specs = tree_util.tree_map(jax_arg_spec_from_tf, kwargs_tf)
    kwargs_specs = export.symbolic_args_specs(
        kwargs_jax_specs, None)
    combined_args_tf = (args_tf, kwargs_tf)
    args_flat_tf: Sequence[TfVal]
    args_flat_tf, args_kwargs_tree = tree_util.tree_flatten(combined_args_tf)

    args_flat_tf = tuple(
        map(preprocess_arg_tf, range(len(args_flat_tf)), args_flat_tf))

    impl = NativeSerializationImpl(
        fun_jax,
        args_specs=args_specs, kwargs_specs=kwargs_specs,
        native_serialization_platforms=native_serialization_platforms,
        native_serialization_disabled_checks=native_serialization_disabled_checks)
    try:
      impl.before_conversion()

      outs_tree: tree_util.PyTreeDef | None = None
      if with_gradient:
        @tf.custom_gradient
        def converted_fun_flat_with_custom_gradient_tf(*args_flat_tf: TfVal) -> TfVal:
          nonlocal outs_tree
          outs_tf, outs_avals, outs_tree = impl.run_fun_tf(args_flat_tf)
          return (tuple(outs_tf),
                  _make_custom_gradient_fn_tf(
                      fun_jax,
                      impl=impl,
                      with_gradient=with_gradient,
                      args_specs=args_specs, kwargs_specs=kwargs_specs,
                      args_tf=args_flat_tf,
                      outs_avals=outs_avals,
                      outs_tf=outs_tf))

        outs_flat_tf = converted_fun_flat_with_custom_gradient_tf(*args_flat_tf)
      else:
        outs_tf, _, outs_tree = impl.run_fun_tf(args_flat_tf)
        message = ("The jax2tf-converted function does not support gradients. "
                   "Use `with_gradient` parameter to enable gradients")
        # We use PreventGradient, which is propagated through a SavedModel.
        outs_flat_tf = [
            tf.raw_ops.PreventGradient(input=o, message=message)
            for o in outs_tf
        ]
    finally:
      impl.after_conversion()

    assert outs_tree is not None
    outs_flat_tf = [tf.identity(x, "jax2tf_out") for x in outs_flat_tf]
    out_tf = tree_util.tree_unflatten(outs_tree, outs_flat_tf)
    return out_tf

  return converted_fun_tf


def convert(credentials):
    """Convert oauth2client credentials to google-auth credentials.

    This class converts:

    - :class:`oauth2client.client.OAuth2Credentials` to
      :class:`google.oauth2.credentials.Credentials`.
    - :class:`oauth2client.client.GoogleCredentials` to
      :class:`google.oauth2.credentials.Credentials`.
    - :class:`oauth2client.service_account.ServiceAccountCredentials` to
      :class:`google.oauth2.service_account.Credentials`.
    - :class:`oauth2client.service_account._JWTAccessCredentials` to
      :class:`google.oauth2.service_account.Credentials`.
    - :class:`oauth2client.contrib.gce.AppAssertionCredentials` to
      :class:`google.auth.compute_engine.Credentials`.
    - :class:`oauth2client.contrib.appengine.AppAssertionCredentials` to
      :class:`google.auth.app_engine.Credentials`.

    Returns:
        google.auth.credentials.Credentials: The converted credentials.

    Raises:
        ValueError: If the credentials could not be converted.
    """

    credentials_class = type(credentials)

    try:
        return _CLASS_CONVERSION_MAP[credentials_class](credentials)
    except KeyError as caught_exc:
        new_exc = ValueError(_CONVERT_ERROR_TMPL.format(credentials_class))
        raise new_exc from caught_exc

