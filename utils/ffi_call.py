
def ffi_call(
    target_name: str,
    result_shape_dtypes: ResultMetadata,
    *,
    has_side_effect: bool = ...,
    vmap_method: str | None = ...,
    input_layouts: Sequence[FfiLayoutOptions] | None = ...,
    output_layouts: FfiLayoutOptions | Sequence[FfiLayoutOptions] | None = ...,
    input_output_aliases: dict[int, int] | None = ...,
    custom_call_api_version: int = ...,
    legacy_backend_config: str | None = ...,
) -> Callable[..., Array]:
  ...


def ffi_call(
    target_name: str,
    result_shape_dtypes: Sequence[ResultMetadata],
    *,
    has_side_effect: bool = ...,
    vmap_method: str | None = ...,
    input_layouts: Sequence[FfiLayoutOptions] | None = ...,
    output_layouts: FfiLayoutOptions | Sequence[FfiLayoutOptions] | None = ...,
    input_output_aliases: dict[int, int] | None = ...,
    custom_call_api_version: int = ...,
    legacy_backend_config: str | None = ...,
) -> Callable[..., Sequence[Array]]:
  ...


def ffi_call(
    target_name: str,
    result_shape_dtypes: ResultMetadata | Sequence[ResultMetadata],
    *,
    has_side_effect: bool = False,
    vmap_method: str | None = None,
    input_layouts: Sequence[FfiLayoutOptions] | None = None,
    output_layouts: FfiLayoutOptions | Sequence[FfiLayoutOptions] | None = None,
    input_output_aliases: dict[int, int] | None = None,
    custom_call_api_version: int = 4,
    legacy_backend_config: str | None = None,
) -> Callable[..., Array | Sequence[Array]]:
  """Call a foreign function interface (FFI) target.

  See the :ref:`ffi-tutorial` tutorial for more information.

  Like :func:`~jax.pure_callback`, the behavior of ``ffi_call`` under
  :func:`~jax.vmap` depends on the value of ``vmap_method``. See the
  :func:`~jax.pure_callback` documentation for more details about the allowed
  values and examples of their behavior.

  The current default behavior is to use ``vmap_method="sequential"`` when
  not specified, but this behavior is deprecated, and in the future, the
  default will be to raise a ``NotImplementedError`` unless ``vmap_method`` is
  explicitly specified.

  Args:
    target_name: the name of the XLA FFI custom call target that was registered
      using :func:`~jax.ffi.register_ffi_target`.
    result_shape_dtypes: an object, or sequence of objects, with ``shape`` and
      ``dtype`` attributes which are expected to match the shape and dtype of
      the custom call output or outputs. :class:`~jax.ShapeDtypeStruct` is often
      used to define the elements of ``result_shape_dtypes``.
      ``jax.core.abstract_token`` may be used to represent a token-typed output.
    has_side_effect: boolean specifying whether the custom call has side
      effects. When ``True``, the FFI call will be executed even when the
      outputs are not used.
    vmap_method: string specifying how the FFI call transforms under
      :func:`~jax.vmap` as described above.
    input_layouts: a sequence of layouts for each input argument. In each case,
      the layout can be (a) ``None`` indicating that this input is in default
      row-major order, (b) a ``Layout`` specifying the axis order,
      or (c) a sequence of integers specifying the major-to-minor axis
      ordering. Users who are familiar with XLA layouts should note that this
      function expects layouts in major-to-minor order instead of the
      minor-to-major order that XLA uses. For example, a batch of row-major
      matrices could be specified using the layout ``[0, 1, 2]``, whereas a
      batch of column-major matrices would have layout ``[0, 2, 1]``. In both
      of these examples, the leading/batch dimension is the "slowest" axis. The
      ``input_layouts`` parameter should be used to request the memory layout
      expected by the FFI call target, and XLA will ensure that the buffers
      have the correct layouts before the handler is executed.
    output_layouts: like ``input_layouts``, but specifying the required layouts
      for the output arrays.
    input_output_aliases: a dictionary where the keys are input indices and the
      values are output indices. This mapping indicates which output arrays
      alias specific input arrays.
    custom_call_api_version: the version number of the custom call API
      implemented by the FFI target ``target_name``. The only formally
      supported version is the typed FFI API with ``custom_call_api_version=4``,
      but earlier unsupported custom calls can be executed using this argument.
    legacy_backend_config: for legacy targets implemented using
      ``custom_call_api_version<4``, attributes are passed using the opaque
      string representation provided by this argument. This parameter cannot be
      used with ``custom_call_api_version>=4``.

  Returns:
    A function that can be called with the input arrays as positional arguments
    to execute the FFI handler. Any keyword arguments are passed as named
    attributes to the FFI handler using XLA's FFI interface.
  """

  allowed_vmap_methods = ["sequential", "sequential_unrolled", "expand_dims",
                          "broadcast_all", "legacy_vectorized", None]
  if vmap_method not in allowed_vmap_methods:
    raise ValueError(
        f"vmap_method must be on of the allowed methods {allowed_vmap_methods}, "
        f"but got: {vmap_method}")

  output_layouts_: Sequence[FfiLayoutOptions] | None
  if isinstance(result_shape_dtypes, Sequence):
    output_layouts_ = output_layouts  # pyrefly: ignore[bad-assignment]
    multiple_results = True
    result_avals = _result_avals(result_shape_dtypes)
  else:
    multiple_results = False
    result_avals = _result_avals([result_shape_dtypes])
    output_layouts_ = (output_layouts,)  # pyrefly: ignore[bad-assignment]

  if custom_call_api_version >= 4 and legacy_backend_config is not None:
    raise ValueError(
        "The use of the legacy_backend_config parameter requires "
        f"custom_call_api_version < 4; got {custom_call_api_version}.")

  def wrapped(*args: ArrayLike, **kwargs: Any):
    in_avals = [core.typeof(x) for x in args]

    if input_layouts is None:
      static_input_layouts = tuple(map(_convert_layout_for_lowering, in_avals))
    else:
      if len(input_layouts) != len(in_avals):
        raise ValueError(
            f"The number of input arguments ({len(in_avals)}) must equal the "
            f"number of input layouts ({len(input_layouts)}).")
      static_input_layouts = _convert_layouts_for_ffi_call(in_avals,
                                                           input_layouts)
    if output_layouts_ is None:
      static_output_layouts = tuple(map(_convert_layout_for_lowering,
                                        result_avals))
    else:
      if len(output_layouts_) != len(result_avals):
        raise ValueError(
            f"The number of outputs ({len(result_avals)}) must equal the "
            f"number of output layouts ({len(output_layouts_)}).")
      static_output_layouts = _convert_layouts_for_ffi_call(result_avals,
                                                            output_layouts_)

    static_input_output_aliases: list[tuple[int, int]] = []
    if input_output_aliases is not None:
      for i_idx, o_idx in sorted(input_output_aliases.items()):
        i_idx, o_idx = int(i_idx), int(o_idx)
        if i_idx >= len(args):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"with input index {i_idx} outside the range [0, "
              f"{len(args)}).")
        if o_idx >= len(result_avals):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"with output index {o_idx} outside the range [0, "
              f"{len(result_avals)}).")
        in_aval = in_avals[i_idx]
        out_aval = result_avals[o_idx]
        if not _check_compatible_avals(in_aval, out_aval):
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"referring to an input with abstract value {in_aval} and an "
              f"output with a different abstract value {out_aval}.")
        if static_input_layouts[i_idx] != static_output_layouts[o_idx]:
          raise ValueError(
              f"input_output_aliases contains the mapping '{i_idx}:{o_idx}' "
              f"referring to an input with layout {static_input_layouts[i_idx]} "
              "and an output with a different layout "
              f"{static_output_layouts[o_idx]}.")
        static_input_output_aliases.append((i_idx, o_idx))
    args = core.auto_insert_reshard(*args)
    results = ffi_call_p.bind(
        *args,
        result_avals=result_avals,
        vmap_method=vmap_method,
        target_name=target_name,
        has_side_effect=has_side_effect,
        input_layouts=static_input_layouts,
        output_layouts=static_output_layouts,
        input_output_aliases=tuple(static_input_output_aliases),
        custom_call_api_version=custom_call_api_version,
        legacy_backend_config=legacy_backend_config,
        attributes=_wrap_kwargs_hashable(kwargs),
    )
    if multiple_results:
      if isinstance(result_shape_dtypes, tuple):
        return tuple(results)
      return results
    else:
      return results[0]

  return wrapped

