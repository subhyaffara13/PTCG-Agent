
def _is_clang(cpp_compiler: str) -> bool:
    # Mac OS apple clang maybe named as gcc, need check compiler info.
    if sys.platform == "darwin":
        return _is_apple_clang(cpp_compiler)
    elif _IS_WINDOWS:
        # clang suite have many compilers, and only clang-cl is supported.
        if re.search(r"((clang$)|(clang\+\+$))", cpp_compiler):
            raise RuntimeError(
                "Please use clang-cl, due to torch.compile only support MSVC-like CLI (compiler flags syntax)."
            )
        return bool(re.search(r"(clang-cl)", cpp_compiler))
    return bool(re.search(r"(clang|clang\+\+)", cpp_compiler))

