
def preparse_sysargv():
    # To keep backwards bug compatibility, newer flags are handled by argparse,
    # and `sys.argv` is passed to the rest of `f2py` as is.
    parser = make_f2py_compile_parser()

    args, remaining_argv = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining_argv

    backend_key = args.backend
    if backend_key == 'distutils':
        outmess("Cannot use distutils backend with Python>=3.12,"
                " using meson backend instead.\n")
        backend_key = "meson"

    return {
        "dependencies": args.dependencies or [],
        "backend": backend_key,
        "modulename": args.module_name,
    }

