
def _src_path_is_module(src_path: Path, module_name: str) -> bool:
    return (
        module_name == src_path.name and src_path.is_dir() and exists_case_sensitive(str(src_path))
    )

