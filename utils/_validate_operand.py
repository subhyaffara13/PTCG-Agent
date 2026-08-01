
def _validate_operand(obj: DataFrame | Series) -> DataFrame:
    if isinstance(obj, ABCDataFrame):
        return obj
    elif isinstance(obj, ABCSeries):
        if obj.name is None:
            raise ValueError("Cannot merge a Series without a name")
        return obj.to_frame()
    else:
        raise TypeError(
            f"Can only merge Series or DataFrame objects, a {type(obj)} was passed"
        )

