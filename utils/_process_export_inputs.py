from typing import Callable

def _process_export_inputs(
    mod: torch.nn.Module,
    args: tuple[object, ...],
    kwargs: dict[str, object] | None,
    dynamic_shapes: _DynamicShapesSpec
    | torch.export.AdditionalInputs
    | torch.export.ShapesCollection
    | None,
) -> tuple[
    tuple[object, ...],
    dict[str, object],
    TreeSpec,
    _DynamicShapesSpec | None,
    Callable[[ExportedProgram], None],
]:
    """
    Process and validate export inputs for the torch.export API.

    This function validates the input arguments, normalizes kwargs, computes input tree specs,
    and handles special dynamic shapes cases like AdditionalInputs and ShapesCollection.

    Args:
        mod: The PyTorch module to be exported.
        args: Tuple of example positional inputs for the module.
        kwargs: Optional dictionary of example keyword inputs.
        dynamic_shapes: Optional specification for dynamic shapes. Can be:
            - dict mapping argument names to dynamic shape specifications
            - tuple/list specifying dynamic shapes for each input in order
            - torch.export.AdditionalInputs object with verification callback
            - torch.export.ShapesCollection object

    Returns:
        A tuple containing:
        - args: Validated tuple of positional inputs
        - kwargs: Normalized dictionary of keyword inputs (empty dict if None was passed)
        - original_in_spec: TreeSpec representing the flattened input structure
        - dynamic_shapes: Processed dynamic shapes specification
        - verify_additional_inputs: Callback function for additional input verification

    Raises:
        UserError: If args is not a tuple.
    """
    if not isinstance(args, tuple):
        raise UserError(
            UserErrorType.INVALID_INPUT,
            f"Expecting `args` to be a tuple of example positional inputs, got {type(args)}",
        )
    kwargs = kwargs if kwargs is not None else {}
    if pytree.is_namedtuple_instance(args):
        args = tuple(args)

    _, original_in_spec = pytree.tree_flatten((args, kwargs))

    verify_additional_inputs: Callable[[ExportedProgram], None]
    out_dynamic_shapes: _DynamicShapesSpec | None
    if isinstance(dynamic_shapes, torch.export.AdditionalInputs):
        verify_additional_inputs = dynamic_shapes.verify  # type: ignore[assignment]
        out_dynamic_shapes = dynamic_shapes.dynamic_shapes(mod, args, kwargs)  # type: ignore[assignment]
    else:
        verify_additional_inputs = lambda ep: None  # noqa: E731
        if isinstance(dynamic_shapes, torch.export.ShapesCollection):
            out_dynamic_shapes = dynamic_shapes.dynamic_shapes(mod, args, kwargs)  # type: ignore[assignment]
        else:
            out_dynamic_shapes = dynamic_shapes

    return args, kwargs, original_in_spec, out_dynamic_shapes, verify_additional_inputs

