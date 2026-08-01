
def raise_error_container_parameter_missing(target_type) -> None:
    if target_type.endswith("ict"):
        raise RuntimeError(
            f"Attempted to use {target_type} without "
            "contained types. Please add contained type, e.g. "
            f"{target_type}[int, int]"
        )
    raise RuntimeError(
        f"Attempted to use {target_type} without a "
        "contained type. Please add a contained type, e.g. "
        f"{target_type}[int]"
    )

