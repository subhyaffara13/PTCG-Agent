
def node_proto(
    name: str,
    op: str = "UnSpecified",
    input: list[str] | str | None = None,
    dtype: torch.dtype | None = None,
    shape: tuple[int, ...] | None = None,
    outputsize: Sequence[int] | None = None,
    attributes: str = "",
) -> NodeDef:
    """Create an object matching a NodeDef.

    Follows https://github.com/tensorflow/tensorboard/blob/master/tensorboard/compat/proto/node_def.proto .
    """
    if input is None:
        input = []
    if not isinstance(input, list):
        input = [input]
    return NodeDef(
        name=name.encode(encoding="utf_8"),
        op=op,
        input=input,
        attr=attr_value_proto(dtype, outputsize, attributes),
    )

