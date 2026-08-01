
def _get_cpp_std_cflag(std_num: str = "c++20") -> list[str]:
    if _IS_WINDOWS:
        """
        On Windows, only c++20 can support `std::enable_if_t`.
        Ref: https://learn.microsoft.com/en-us/cpp/overview/cpp-conformance-improvements-2019?view=msvc-170#checking-for-abstract-class-types # noqa: B950
        Note:
            Only setup c++20 for Windows inductor. I tried to upgrade all project to c++20, but it is failed:
            https://github.com/pytorch/pytorch/pull/131504
        """
        std_num = "c++20"
        return [f"std:{std_num}"]
    else:
        return [f"std={std_num}"]

