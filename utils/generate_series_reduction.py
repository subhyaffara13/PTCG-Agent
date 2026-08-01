
def generate_series_reduction(ser_reduction, ser_method):
    @overload_method(SeriesType, ser_reduction)
    def series_reduction(series):
        def series_reduction_impl(series):
            return ser_method(series.values)

        return series_reduction_impl

    return series_reduction

