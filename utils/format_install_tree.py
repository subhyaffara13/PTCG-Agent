
def format_install_tree(tree):
    return {
        x.format(
            py_version=sysconfig.get_python_version(),
            platform=get_platform(),
            shlib_ext=get_config_var('EXT_SUFFIX') or get_config_var('SO'),
        )
        for x in tree
    }

