
def check_args_exist(target_type) -> None:
    if name := _RAW_TYPE_NAME_MAPPING.get(target_type):
        raise_error_container_parameter_missing(name)

