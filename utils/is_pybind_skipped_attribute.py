
def is_pybind_skipped_attribute(attr: str) -> bool:
    return attr.startswith("__pybind11_module_local_")

