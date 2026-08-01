
def get_dependencies_to_install(path, *, dependency_group=None, **kwargs):
    # See https://github.com/pypa/pip/issues/53
    raise Exception("pip is unable to do a dry run")

