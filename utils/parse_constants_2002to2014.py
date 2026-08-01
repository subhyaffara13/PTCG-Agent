
def parse_constants_2002to2014(
    d: str, exact_func: Callable[[Any], Any]
) -> dict[str, tuple[float, str, float]]:
    constants: dict[str, tuple[float, str, float]] = {}
    exact: dict[str, float] = {}
    need_replace = set()
    for line in d.split('\n'):
        name = line[:55].rstrip()
        val = float(line[55:77].replace(' ', '').replace('...', ''))
        is_truncated = '...' in line[55:77]
        is_exact = '(exact)' in line[77:99]
        if is_truncated and is_exact:
            # missing decimals, use computed exact value
            need_replace.add(name)
        elif is_exact:
            exact[name] = val
        else:
            assert not is_truncated
        uncert = float(line[77:99].replace(' ', '').replace('(exact)', '0'))
        units = line[99:].rstrip()
        constants[name] = (val, units, uncert)
    replace = exact_func(exact)
    replace_exact(constants, need_replace, replace)
    return constants

