
def _register_lowering(
    aten_fn,
    decomp_fn: Callable[..., Any],
    broadcast: bool,
    type_promotion_kind: ELEMENTWISE_TYPE_PROMOTION_KIND | None,
    convert_input_to_bool: bool,
    lowering_dict: dict[Callable[..., Any] | str, Callable[..., Any]],
):
    """
    Add a lowering to lowerings dict

    Arguments:
        aten_fn: torch.ops.aten.* fn we are lowering
        decomp_fn: alternate implementation on our IR
        broadcast: True to apply broadcasting to tensor inputs
        type_promotion_kind: kind of type promotion applied to tensor inputs, `None` means no type promotion
        convert_input_to_bool: some logical ops require inputs are converted to bool
    """

    @functools.wraps(decomp_fn)
    def wrapped(*args, **kwargs):
        args: list[Any] = list(args)
        kwargs: dict[str, Any] = dict(kwargs)
        unpacked = False
        # TODO maybe we need to use pytrees here
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            unpacked = True
            args = list(args[0])

        if not all(
            (fn in fallbacks or in_namespace(fn, "_c10d_functional")) for fn in aten_fn
        ):
            # explicitly assert for "out=" ops for better error messages
            assert not any(x == "out" for x in kwargs), "out= ops aren't yet supported"

        args, kwargs = transform_args(
            args, kwargs, broadcast, type_promotion_kind, convert_input_to_bool
        )

        if unpacked:
            args = [args]

        out = decomp_fn(*args, **kwargs)
        validate_ir(out)

        return out

    aten_fn = get_overloads(aten_fn)

    lowering_dict.update(dict.fromkeys(aten_fn, wrapped))
    return wrapped


def _register_lowering(
    op: str | type[ir.OpView] | None,
    support_warp_semantics: bool = False,
) -> Callable[[MlirLoweringRule], MlirLoweringRule]:
  def wrapper(f):
    if op is not None:
      op_name = op if isinstance(op, str) else op.OPERATION_NAME  # pyrefly: ignore[missing-attribute]
      _lowerings[op_name] = f
      if support_warp_semantics:
        _supported_warp_lowerings.add(op_name)
    return f

  return wrapper

