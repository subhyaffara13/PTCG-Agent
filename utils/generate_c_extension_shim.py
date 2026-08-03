import os

def generate_c_extension_shim(
    full_module_name: str, module_name: str, dir_name: str, group_name: str
) -> str:
    """Create a C extension shim with a passthrough PyInit function.

    Arguments:
        full_module_name: the dotted full module name
        module_name: the final component of the module name
        dir_name: the directory to place source code
        group_name: the name of the group
    """
    cname = "%s.c" % full_module_name.replace(".", os.sep)
    cpath = os.path.join(dir_name, cname)

    if IS_FREE_THREADED:
        # We use multi-phase init in free-threaded builds to enable free threading.
        shim_name = "module_shim_no_gil_multiphase.tmpl"
    else:
        shim_name = "module_shim.tmpl"

    # We load the C extension shim template from a file.
    # (So that the file could be reused as a bazel template also.)
    with open(os.path.join(include_dir(), shim_name)) as f:
        shim_template = f.read()

    write_file(
        cpath,
        shim_template.format(
            modname=module_name,
            libname=shared_lib_name(group_name),
            full_modname=exported_name(full_module_name),
        ),
    )

    return cpath

