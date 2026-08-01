
def parse_positional_flags(source, info, flags_on, flags_off):
    "Parses positional flags."
    info.flags = (info.flags | flags_on) & ~flags_off
    source.ignore_space = bool(info.flags & VERBOSE)

