
def f2py_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-I", dest="include_paths", action=CombineIncludePaths)
    parser.add_argument("--include-paths", dest="include_paths", action=CombineIncludePaths)
    parser.add_argument("--include_paths", dest="include_paths", action=CombineIncludePaths)
    parser.add_argument("--freethreading-compatible", dest="ftcompat", action=argparse.BooleanOptionalAction)
    return parser

