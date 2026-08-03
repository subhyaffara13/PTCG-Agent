import pathlib

def check_nnapi_partitions(model, require_fixed_input_sizes: bool):
    # if we're running in the ORT python package the file should be local. otherwise assume we're running from the
    # ORT repo
    script_dir = pathlib.Path(__file__).parent
    local_config = script_dir / "nnapi_supported_ops.md"
    if local_config.exists():
        config_path = local_config
    else:
        ort_root = script_dir.parents[3]
        config_path = ort_root / "tools" / "ci_build" / "github" / "android" / "nnapi_supported_ops.md"

    return _check_ep_partitioning(model, config_path, require_fixed_input_sizes)

