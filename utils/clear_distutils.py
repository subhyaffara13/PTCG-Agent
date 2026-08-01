
def clear_distutils():
    if 'distutils' not in sys.modules:
        return
    import warnings

    warnings.warn(
        "Setuptools is replacing distutils. Support for replacing "
        "an already imported distutils is deprecated. In the future, "
        "this condition will fail. "
        f"Register concerns at {report_url}"
    )
    mods = [
        name
        for name in sys.modules
        if name == "distutils" or name.startswith("distutils.")
    ]
    for name in mods:
        del sys.modules[name]

