
def test_attributes_module(module_name):
    """
    Ensures that all public objects have their __module__ set to the public import path.
    """
    recurse = module_name not in ["pandas", "pandas.testing"]
    objs = get_pandas_objects(module_name, recurse=recurse)
    failures = [
        (module_name, name, type(obj), obj.__module__)
        for module_name, name, obj in objs
        if not (
            obj.__module__ == module_name
            # Explicit exceptions
            or ("Dtype" in name and obj.__module__ == "pandas")
            or (name == "Categorical" and obj.__module__ == "pandas")
        )
    ]
    assert len(failures) == 0, "\n".join(str(e) for e in failures)

    # Check that all objects can indeed be imported from their __module__
    failures = []
    for module_name, name, obj in objs:
        module = importlib.import_module(obj.__module__)
        try:
            getattr(module, name)
        except Exception:
            failures.append((module_name, name, type(obj), obj.__module__))
    assert len(failures) == 0, "\n".join(str(e) for e in failures)

