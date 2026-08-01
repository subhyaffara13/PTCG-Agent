
def generate_series_binop(binop):
    @overload(binop)
    def series_binop(series1, value):
        if isinstance(series1, SeriesType):
            if isinstance(value, SeriesType):

                def series_binop_impl(series1, series2):
                    # TODO: Check index matching?
                    return Series(
                        binop(series1.values, series2.values),
                        series1.index,
                        series1.name,
                    )

                return series_binop_impl
            else:

                def series_binop_impl(series1, value):
                    return Series(
                        binop(series1.values, value), series1.index, series1.name
                    )

                return series_binop_impl

    return series_binop

