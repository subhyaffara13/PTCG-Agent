
def _quarterly_finder(vmin: float, vmax: float, freq: BaseOffset) -> np.ndarray:
    _, _, periodsperyear = _get_periods_per_ymd(freq)
    vmin_orig = vmin
    (vmin, vmax) = (int(vmin), int(vmax))
    span = vmax - vmin + 1

    info = np.zeros(
        span, dtype=[("val", int), ("maj", bool), ("min", bool), ("fmt", "|S8")]
    )
    info["val"] = np.arange(vmin, vmax + 1)
    info["fmt"] = ""
    dates_ = info["val"]
    info_maj = info["maj"]
    info_fmt = info["fmt"]
    year_start = (dates_ % 4 == 0).nonzero()[0]

    if span <= 3.5 * periodsperyear:
        info_maj[year_start] = True
        info["min"] = True

        info_fmt[:] = "Q%q"
        info_fmt[year_start] = "Q%q\n%F"
        if not has_level_label(year_start, vmin_orig):
            if dates_.size > 1:
                idx = 1
            else:
                idx = 0
            info_fmt[idx] = "Q%q\n%F"

    elif span <= 11 * periodsperyear:
        info_maj[year_start] = True
        info["min"] = True
        info_fmt[year_start] = "%F"

    else:
        # https://github.com/pandas-dev/pandas/pull/47602
        years = dates_[year_start] // 4 + 1970
        nyears = span / periodsperyear
        (min_anndef, maj_anndef) = _get_default_annual_spacing(nyears)
        major_idx = year_start[(years % maj_anndef == 0)]
        info_maj[major_idx] = True
        info["min"][year_start[(years % min_anndef == 0)]] = True
        info_fmt[major_idx] = "%F"

    return info

