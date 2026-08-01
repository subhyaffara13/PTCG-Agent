
def parse_constants_2018toXXXX(
    d: str, exact_func: Callable[[Any], Any]
) -> dict[str, tuple[float, str, float]]:
    constants: dict[str, tuple[float, str, float]] = {}
    exact: dict[str, float] = {}
    need_replace = set()
    for line in d.split('\n'):
        name = line[:60].rstrip()
        val = float(line[60:85].replace(' ', '').replace('...', ''))
        is_truncated = '...' in line[60:85]
        is_exact = '(exact)' in line[85:110]
        if is_truncated and is_exact:
            # missing decimals, use computed exact value
            need_replace.add(name)
        elif is_exact:
            exact[name] = val
        else:
            assert not is_truncated
        uncert = float(line[85:110].replace(' ', '').replace('(exact)', '0'))
        units = line[110:].rstrip()
        constants[name] = (val, units, uncert)
    replace = exact_func(exact)
    replace_exact(constants, need_replace, replace)
    return constants

