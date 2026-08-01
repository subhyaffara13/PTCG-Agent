
def exclude_callback(option, opt, value, parser):
    if EXCLUDE_RE.match(value) is None:
        raise optparse.OptionValueError(f"{opt} argument has invalid value")
    parser.values.exclude = TAG_RE.findall(value)

