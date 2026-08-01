
def get_newer_options(iline):
    iline = (' '.join(iline)).split()
    parser = f2py_parser()
    args, remain = parser.parse_known_args(iline)
    ipaths = args.include_paths
    if args.include_paths is None:
        ipaths = []
    return ipaths, args.ftcompat, remain

