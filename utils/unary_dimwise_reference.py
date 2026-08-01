
def unary_dimwise_reference(op, sample, batchwise_reference=None):
    # extract info about the dim args this op supports
    if op._extra_op_data.dim_args is None:
        raise AssertionError("Expected op._extra_op_data.dim_args to not be None")
    single_dim_argname, dimlist_argname = op._extra_op_data.get_dim_argnames()
    # only support a single non-list dim arg for now
    if dimlist_argname is not None:
        raise AssertionError("Expected dimlist_argname to be None")
    if single_dim_argname is None:
        raise AssertionError("Expected single_dim_argname to not be None")
    if sample.kwargs[single_dim_argname] == 0:
        # unbind reference won't work for batch-wise operation; handle this case here
        if batchwise_reference is None:
            raise AssertionError("Expected batchwise_reference to not be None")
        return batchwise_reference(op, sample)
    return unbind_reference(op, sample)

