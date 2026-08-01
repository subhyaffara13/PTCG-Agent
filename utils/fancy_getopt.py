
def fancy_getopt(options, negative_opt, object, args: Sequence[str] | None):
    parser = FancyGetopt(options)
    parser.set_negative_aliases(negative_opt)
    return parser.getopt(args, object)

