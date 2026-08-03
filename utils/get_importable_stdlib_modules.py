import sys

def get_importable_stdlib_modules() -> set[str]:
    """Return all importable stdlib modules at runtime."""
    importable_stdlib_modules: set[str] = set()
    for module_name in sys.stdlib_module_names:
        if module_name in ANNOYING_STDLIB_MODULES:
            continue

        try:
            runtime = silent_import_module(module_name)
        except ImportError:
            continue
        else:
            importable_stdlib_modules.add(module_name)

        try:
            # some stdlib modules (e.g. `nt`) don't have __path__ set...
            runtime_path = runtime.__path__
            runtime_name = runtime.__name__
        except AttributeError:
            continue

        for submodule in pkgutil.walk_packages(runtime_path, runtime_name + "."):
            submodule_name = submodule.name

            # There are many annoying *.__main__ stdlib modules,
            # and including stubs for them isn't really that useful anyway:
            # tkinter.__main__ opens a tkinter windows; unittest.__main__ raises SystemExit; etc.
            #
            # The idlelib.* submodules are similarly annoying in opening random tkinter windows,
            # and we're unlikely to ever add stubs for idlelib in typeshed
            # (see discussion in https://github.com/python/typeshed/pull/9193)
            #
            # test.* modules do weird things like raising exceptions in __del__ methods,
            # leading to unraisable exceptions being logged to the terminal
            # as a warning at the end of the stubtest run
            if submodule_name.endswith(".__main__") or submodule_name.startswith(
                ("idlelib.", "test.")
            ):
                continue

            try:
                silent_import_module(submodule_name)
            except KeyboardInterrupt:
                raise
            # importing multiprocessing.popen_forkserver on Windows raises AttributeError...
            # some submodules also appear to raise SystemExit as well on some Python versions
            # (not sure exactly which)
            except BaseException:
                continue
            else:
                importable_stdlib_modules.add(submodule_name)

    return importable_stdlib_modules

