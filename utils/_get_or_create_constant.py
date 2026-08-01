
def _get_or_create_constant(
    constant_farm: dict[
        tuple[
            bool
            | int
            | float
            | str
            | tuple[int, ...]
            | tuple[float, ...]
            | tuple[bool, ...],
            ir.DataType,
        ],
        ir.Value,
    ],
    arg: bool
    | int
    | float
    | str
    | tuple[int, ...]
    | tuple[float, ...]
    | tuple[bool, ...]
    | list[int]
    | list[float]
    | list[bool],
    dtype: ir.DataType,
    opset: onnxscript.values.Opset,
) -> ir.Value:
    # float representation of complex numbers
    if isinstance(arg, complex):
        # Convert the complex number to a float
        arg = (arg.real, arg.imag)

    if isinstance(arg, list):
        # Make the arg hashable
        # pyrefly: ignore [bad-argument-type]
        arg = tuple(arg)

    constant_value = constant_farm.get((arg, dtype))  # type: ignore[arg-type]
    if constant_value is None:
        constant_tensor = ir.tensor(value=arg, dtype=dtype)
        constant_value = opset.Constant(value=constant_tensor)
        constant_farm[(arg, dtype)] = constant_value  # type: ignore[arg-type,index]
    return constant_value  # type: ignore[return-value]

