
def symbolic(
    domain_op: str,
    /,
    inputs: Sequence[torch.Tensor | None],
    attrs: dict[
        str,
        int
        | float
        | str
        | bool
        | Sequence[int]
        | Sequence[float]
        | Sequence[str]
        | Sequence[bool],
    ]
    | None = None,
    *,
    dtype: torch.dtype | int,
    shape: Sequence[int | torch.SymInt],
    version: int | None = None,
    metadata_props: dict[str, str] | None = None,
) -> torch.Tensor:
    """Create a symbolic FX operator to represent an arbitrary ONNX operator.

    This function is used to create a symbolic operator with a single output.
    To create an operator with multiple outputs, use :func:`symbolic_multi_out`.

    You may use ``if torch.onnx.is_in_onnx_export()`` to conditionally enable the
    symbolic logic only during ``torch.onnx.export()``.

    Example::

        class CustomOp(torch.nn.Module):
            def forward(self, x: torch.Tensor) -> torch.Tensor:
                # Normal torch operators can interleave with the symbolic ops during ONNX export
                x = x + 1

                # Create a symbolic ONNX operator with the name "CustomOp" in the "custom_domain" domain.
                # The output tensor will have the specified dtype and shape
                val = torch.onnx.ops.symbolic(
                    "custom_domain::CustomOp",
                    (x,),
                    dict(attr_key="attr_value"),
                    dtype=x.dtype,
                    shape=x.shape,
                    version=1,
                )

                # The result of the symbolic op can be used in normal torch operations during ONNX export
                return torch.nn.functional.relu(val)


        # You may then export this model to ONNX using torch.onnx.export(..., dynamo=True).

    Args:
        domain_op: The domain and operator name, separated by "::". For example,
            "custom_domain::CustomOp".
        inputs: The input tensors to the operator.
        attrs: The attributes of the operator. The keys are attribute names and
            the values are attribute values. Valid attribute types are int, float,
            str, bool, and lists of int, float, str, and bool. Tensor attributes
            are unsupported.
        dtype: The data type of the output tensor.This can be either a torch.dtype
            or an integer representing the ONNX data type.
        shape: The shape of the output tensor. This can be a list of integers or
            SymInt values.
        version: The version of the opset used for the operator.
        metadata_props: Metadata properties for the ONNX node.
            This is a dictionary of str-str pairs.

    Returns:
        The output tensor of the operator.
    """
    if not isinstance(dtype, int):
        torch._check(
            dtype in _TORCH_DTYPE_TO_ONNX_DTYPE, lambda: f"Unsupported dtype: {dtype}"
        )
        dtype = _TORCH_DTYPE_TO_ONNX_DTYPE[dtype]
    domain, op_type = _parse_domain_op_type(domain_op)
    if attrs is None:
        attrs = {}
    encoded_attrs = _symbolic_impl.EncodedAttrs.from_dict(attrs)
    # TODO: Parse domain
    return _symbolic_impl._symbolic(
        inputs,
        op_type,
        dtype,
        shape=shape,
        attr_keys=encoded_attrs.attr_keys,
        attr_types=encoded_attrs.attr_types,
        attr_pos=encoded_attrs.attr_pos,
        attr_ints=encoded_attrs.attr_ints,
        attr_floats=encoded_attrs.attr_floats,
        attr_strs=encoded_attrs.attr_strs,
        metadata_props_keys=metadata_props.keys() if metadata_props else [],
        metadata_props_values=metadata_props.values() if metadata_props else [],
        domain=domain,
        version=version,
    )

