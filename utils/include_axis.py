
def include_axis(op_name: Literal["agg", "apply"], colg: Series | DataFrame) -> bool:
    return isinstance(colg, ABCDataFrame) or (
        isinstance(colg, ABCSeries) and op_name == "agg"
    )

