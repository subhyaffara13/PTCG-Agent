
def get_finder(freq: BaseOffset):
    # error: "BaseOffset" has no attribute "_period_dtype_code"
    dtype_code = freq._period_dtype_code  # type: ignore[attr-defined]
    fgroup = FreqGroup.from_period_dtype_code(dtype_code)

    if fgroup == FreqGroup.FR_ANN:
        return _annual_finder
    elif fgroup == FreqGroup.FR_QTR:
        return _quarterly_finder
    elif fgroup == FreqGroup.FR_MTH:
        return _monthly_finder
    elif (dtype_code >= FreqGroup.FR_BUS.value) or fgroup == FreqGroup.FR_WK:  # pyright: ignore[reportAttributeAccessIssue]
        return _daily_finder
    else:  # pragma: no cover
        raise NotImplementedError(f"Unsupported frequency: {dtype_code}")

