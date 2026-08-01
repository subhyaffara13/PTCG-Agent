
def make_target_python(options: Values) -> TargetPython:
    target_python = TargetPython(
        platforms=options.platforms,
        py_version_info=options.python_version,
        abis=options.abis,
        implementation=options.implementation,
    )

    return target_python

