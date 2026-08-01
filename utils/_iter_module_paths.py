
def _iter_module_paths() -> t.Iterator[str]:
    """Find the filesystem paths associated with imported modules."""
    # List is in case the value is modified by the app while updating.
    for module in list(sys.modules.values()):
        name = getattr(module, "__file__", None)

        if name is None or name.startswith(_ignore_always):
            continue

        while not os.path.isfile(name):
            # Zip file, find the base file without the module path.
            old = name
            name = os.path.dirname(name)

            if name == old:  # skip if it was all directories somehow
                break
        else:
            yield name

