
def maybe_convert_index(ax: Axes, data: NDFrameT) -> NDFrameT:
    # tsplot converts automatically, but don't want to convert index
    # over and over for DataFrames
    if isinstance(data.index, (ABCDatetimeIndex, ABCPeriodIndex)):
        freq = _get_index_freq(data.index)

        if freq is None:
            freq = _get_ax_freq(ax)

        if freq is None:
            raise ValueError("Could not get frequency alias for plotting")

        freq_str = _get_period_alias(freq)

        with warnings.catch_warnings():
            # suppress Period[B] deprecation warning
            # TODO: need to find an alternative to this before the deprecation
            #  is enforced!
            warnings.filterwarnings(
                "ignore",
                r"PeriodDtype\[B\] is deprecated",
                category=FutureWarning,
            )

            if isinstance(data.index, ABCDatetimeIndex):
                data = data.tz_localize(None).to_period(freq=freq_str)
            elif isinstance(data.index, ABCPeriodIndex):
                data.index = data.index.asfreq(freq=freq_str, how="start")
    return data

