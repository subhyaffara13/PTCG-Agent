
def _is_gcc(cpp_compiler: str) -> bool:
    # Since "clang++" ends with "g++", the regex match below would validate on it.
    if _is_clang(cpp_compiler):
        return False
    return bool(re.search(r"(gcc|g\+\+|gnu-c\+\+)", cpp_compiler))

