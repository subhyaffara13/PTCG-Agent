
def _schema_allows_aliasing(func: Any) -> bool:
    schema = func._schema
    # View ops have non-write aliases declared in arguments
    if schema._is_view_op():
        return True
    # Handles cases like mkldnn::_convolution_pointwise_.binary
    # where the schema is Tensor(a!) other -> Tensor(a!) Y
    for ret in schema.returns:
        if ret.alias_info is not None:
            return True
    return False

