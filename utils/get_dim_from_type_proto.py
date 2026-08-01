
def get_dim_from_type_proto(dim):
    return getattr(dim, dim.WhichOneof("value")) if type(dim.WhichOneof("value")) == str else None  # noqa: E721

