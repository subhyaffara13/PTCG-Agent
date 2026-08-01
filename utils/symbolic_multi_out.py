
def symbolic_multi_out(
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
    dtypes: Sequence[torch.dtype | int],
    shapes: Sequence[Sequence[int | torch.SymInt]],
    version: int | None = None,
    metadata_props: dict[str, str] | None = None,
) -> Sequence[torch.Tensor]:
    """Create a symbolic FX operator to represent an arbitrary ONNX operator with multiple outputs.

    You may use ``if torch.onnx.is_in_onnx_export()`` to conditionally enable the
    symbolic logic only during ``torch.onnx.export()``.

    Example::

        class CustomOp(torch.nn.Module):
            def forward(self, x: torch.Tensor) -> torch.Tensor:
                # Normal torch operators can interleave with the symbolic ops during ONNX export
                x = x + 1

                # Create a symbolic ONNX operator with the name "CustomOp" in the "custom_domain" domain.
                # The output tensors will have the specified dtypes and shapes
                (out1, out2) = torch.onnx.ops.symbolic_multi_out(
                    "custom_domain::CustomOp",
                    (x,),
                    dict(attr_key="attr_value"),
                    dtypes=(x.dtype, torch.float32),
                    shapes=(x.shape, [1, 2, 3]),
                    version=1,
                )

                # The result of the symbolic op can be used in normal torch operations during ONNX export
                return torch.nn.functional.relu(out1 + out2)


        # You may then export this model to ONNX using torch.onnx.export(..., dynamo=True).

    Args:
        domain_op: The domain and operator name, separated by "::". For example,
            "custom_domain::CustomOp".
        inputs: The input tensors to the operator.
        attrs: The attributes of the operator. The keys are attribute names and
            the values are attribute values. Valid attribute types are int, float,
            str, bool, and lists of int, float, str, and bool. Tensor attributes
            are unsupported.
        dtypes: The data types of the output tensors. This can be a list of
            torch.dtype or integers representing the ONNX data types. The length
            of this list must be the number of outputs.
        shapes: The shapes of the output tensors. This can be a list of lists of
            integers or SymInt values. The length of this list must be the number of outputs.
        version: The version of the opset used for the operator.
        metadata_props: Metadata properties for the ONNX node.
            This is a dictionary of str-str pairs.

    Returns:
        A list of output tensors of the operator.
    """
    torch._check(
        len(shapes) == len(dtypes),
        lambda: f"Number of shapes ({len(shapes)}) must match number of dtypes ({len(dtypes)})",
    )
    onnx_dtypes = []
    for dtype in dtypes:
        if not isinstance(dtype, int):
            torch._check(
                dtype in _TORCH_DTYPE_TO_ONNX_DTYPE,
                lambda: f"Unsupported dtype: {dtype}",
            )
            onnx_dtypes.append(_TORCH_DTYPE_TO_ONNX_DTYPE[dtype])
        else:
            onnx_dtypes.append(dtype)
    domain, op_type = _parse_domain_op_type(domain_op)
    if attrs is None:
        attrs = {}
    encoded_attrs = _symbolic_impl.EncodedAttrs.from_dict(attrs)
    # Use the size of dtypes to determine the number of outputs
    return _symbolic_impl._symbolic_multi_out(
        inputs,
        op_type,
        onnx_dtypes,
        shapes=shapes,
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

