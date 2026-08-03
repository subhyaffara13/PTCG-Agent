import os

def bdist_wheel_cmd(**kwargs):
    """Run command in the same process so that it is easier to collect coverage"""
    dist_obj = (
        run_setup("setup.py", stop_after="init")
        if os.path.exists("setup.py")
        else Distribution({"script_name": "%%build_meta%%"})
    )
    dist_obj.parse_config_files()
    cmd = bdist_wheel(dist_obj)
    for attr, value in kwargs.items():
        setattr(cmd, attr, value)
    cmd.finalize_options()
    return cmd

