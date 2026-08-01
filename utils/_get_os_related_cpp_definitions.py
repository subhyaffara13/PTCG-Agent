
def _get_os_related_cpp_definitions(cpp_compiler: str) -> list[str]:
    os_definitions: list[str] = []
    if _IS_WINDOWS:
        # On Windows, we need disable min/max macro to avoid C2589 error, as PyTorch CMake:
        # https://github.com/pytorch/pytorch/blob/9a41570199155eee92ebd28452a556075e34e1b4/CMakeLists.txt#L1118-L1119
        os_definitions.append("NOMINMAX")
    return os_definitions

