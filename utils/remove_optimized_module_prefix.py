
def remove_optimized_module_prefix(name: str) -> str:
    return re.sub(r"^_orig_mod[.]", "", name)

