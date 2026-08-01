
def worker(tasks: Queue[str], results: Queue[str | ModuleProperties], sys_path: list[str]) -> None:
    """The main loop of a worker introspection process."""
    sys.path = sys_path
    while True:
        mod = tasks.get()
        try:
            prop = get_package_properties(mod)
        except InspectError as e:
            results.put(str(e))
            continue
        results.put(prop)

