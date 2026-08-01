
def use_dynamic_x(ax: Axes, index: Index) -> bool:
    freq = _get_index_freq(index)
    ax_freq = _get_ax_freq(ax)

    if freq is None:  # convert irregular if axes has freq info
        freq = ax_freq
    # do not use tsplot if irregular was plotted first
    elif (ax_freq is None) and (len(ax.get_lines()) > 0):
        return False

    if freq is None:
        return False

    freq_str = _get_period_alias(freq)

    if freq_str is None:
        return False

    # FIXME: hack this for 0.10.1, creating more technical debt...sigh
    if isinstance(index, ABCDatetimeIndex):
        # error: "BaseOffset" has no attribute "_period_dtype_code"
        freq_str = OFFSET_TO_PERIOD_FREQSTR.get(freq_str, freq_str)
        base = to_offset(freq_str, is_period=True)._period_dtype_code  # type: ignore[attr-defined]
        if base <= FreqGroup.FR_DAY.value:
            return index[:1].is_normalized
        period = Period(index[0], freq_str)
        assert isinstance(period, Period)
        return period.to_timestamp().tz_localize(index.tz) == index[0]
    return True

