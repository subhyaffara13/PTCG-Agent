
def pdseries_constructor(context, builder, sig, args):
    data, index = args
    series = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    series.index = index
    series.values = data
    series.name = context.get_constant(types.intp, 0)
    return impl_ret_borrowed(context, builder, sig.return_type, series._getvalue())

