
def _get_os_related_cpp_cflags(cpp_compiler: str) -> list[str]:
    if _IS_WINDOWS:
        cflags = [
            "wd4819",
            "wd4251",
            "wd4244",
            "wd4267",
            "wd4275",
            "wd4018",
            "wd4190",
            "wd4624",
            "wd4067",
            "wd4068",
            "EHsc",
            # For Intel oneAPI, ref: https://learn.microsoft.com/en-us/cpp/build/reference/zc-cplusplus?view=msvc-170
            "Zc:__cplusplus",
            # Enable max compatible to msvc for oneAPI headers.
            # ref: https://github.com/pytorch/pytorch/blob/db38c44ad639e7ada3e9df2ba026a2cb5e40feb0/cmake/public/utils.cmake#L352-L358 # noqa: B950
            "permissive-",
        ]
    else:
        cflags = ["Wno-unused-variable", "Wno-unknown-pragmas"]
        if _is_clang(cpp_compiler):
            ignored_optimization_argument = (
                "Werror=ignored-optimization-argument"
                if config.aot_inductor.raise_error_on_ignored_optimization
                else "Wno-ignored-optimization-argument"
            )
            cflags.append(ignored_optimization_argument)
        if _is_gcc(cpp_compiler):
            # Issue all the warnings demanded by strict ISO C and ISO C++.
            # Ref: https://github.com/pytorch/pytorch/issues/153180#issuecomment-2986676878
            cflags.append("pedantic")
    return cflags

