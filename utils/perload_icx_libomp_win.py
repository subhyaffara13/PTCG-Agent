import os
import subprocess

def perload_icx_libomp_win(cpp_compiler: str) -> None:
    def _load_icx_built_in_lib_by_name(cpp_compiler: str, lib_name: str) -> bool:
        try:
            output = subprocess.check_output(
                [cpp_compiler, f"-print-file-name={lib_name}"],
                stderr=subprocess.DEVNULL,
            ).decode(*SUBPROCESS_DECODE_ARGS)
            omp_path = output.rstrip()
            if os.path.isfile(omp_path):
                os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
                cdll.LoadLibrary(omp_path)
                return True
        except subprocess.SubprocessError:
            pass
        return False

    """
    Intel Compiler implemented more math libraries than clang, for performance proposal.
    We need preload them like openmp library.
    """
    preload_list = [
        "libiomp5md.dll",  # openmp
        "svml_dispmd.dll",  # svml library
        "libmmd.dll",  # libm
    ]

    for lib_name in preload_list:
        _load_icx_built_in_lib_by_name(cpp_compiler, lib_name)

