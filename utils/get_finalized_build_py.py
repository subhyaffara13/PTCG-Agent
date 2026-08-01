
def get_finalized_build_py(script_name="%build_py-test%"):
    dist = Distribution({"script_name": script_name})
    dist.parse_config_files()
    build_py = dist.get_command_obj("build_py")
    build_py.finalize_options()
    return build_py

