
def _maybe_convert_to_int_keys(convert_dates: dict, varlist: list[Hashable]) -> dict:
    new_dict = {}
    for key, value in convert_dates.items():
        if not value.startswith("%"):  # make sure proper fmts
            convert_dates[key] = "%" + value
        if key in varlist:
            new_dict[varlist.index(key)] = convert_dates[key]
        else:
            if not isinstance(key, int):
                raise ValueError("convert_dates key must be a column or an integer")
            new_dict[key] = convert_dates[key]
    return new_dict

