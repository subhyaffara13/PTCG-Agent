
def write_toplevel_names(cmd, basename, filename) -> None:
    pkgs = dict.fromkeys([
        k.split('.', 1)[0] for k in cmd.distribution.iter_distribution_names()
    ])
    cmd.write_file("top-level names", filename, '\n'.join(sorted(pkgs)) + '\n')

