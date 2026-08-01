
def make_f2py_compile_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--dep", action="append", dest="dependencies")
    parser.add_argument("--backend", choices=['meson', 'distutils'], default='distutils')
    parser.add_argument("-m", dest="module_name")
    return parser

