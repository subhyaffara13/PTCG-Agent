
def _is_apple_clang(cpp_compiler: str) -> bool:
    version_string = subprocess.check_output([cpp_compiler, "--version"]).decode("utf8")
    return "Apple" in version_string.splitlines()[0]

