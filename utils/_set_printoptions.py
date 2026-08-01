
def _set_printoptions(precision=None, threshold=None, edgeitems=None,
                      linewidth=None, suppress=None, nanstr=None,
                      infstr=None, formatter=None, sign=None, floatmode=None,
                      *, legacy=None, override_repr=None):
    new_opt = _make_options_dict(precision, threshold, edgeitems, linewidth,
                                 suppress, nanstr, infstr, sign, formatter,
                                 floatmode, legacy)
    # formatter and override_repr are always reset
    new_opt['formatter'] = formatter
    new_opt['override_repr'] = override_repr

    updated_opt = format_options.get() | new_opt
    updated_opt.update(new_opt)

    if updated_opt['legacy'] == 113:
        updated_opt['sign'] = '-'

    return format_options.set(updated_opt)

