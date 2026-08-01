
def register_plugins(linter: PyLinter, directory: str) -> None:
    """Load all module and package in the given directory, looking for a
    'register' function in each one, used to register pylint checkers.
    """
    imported = {}
    for filename in os.listdir(directory):
        base, extension = os.path.splitext(filename)
        if base in imported or base == "__pycache__":
            continue
        if (extension in PY_EXTS and base != "__init__") or (
            not extension
            and os.path.isdir(os.path.join(directory, base))
            and not filename.startswith(".")
        ):
            try:
                module = modutils.load_module_from_file(
                    os.path.join(directory, filename)
                )
            except ValueError:
                # empty module name (usually Emacs auto-save files)
                continue
            except ImportError as exc:
                print(f"Problem importing module {filename}: {exc}", file=sys.stderr)
            else:
                if hasattr(module, "register"):
                    module.register(linter)
                    imported[base] = 1

