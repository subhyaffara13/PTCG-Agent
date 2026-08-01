
def perload_clang_libomp_win(cpp_compiler: str, omp_name: str) -> None:
    try:
        output = subprocess.check_output([cpp_compiler, "-print-file-name=bin"]).decode(
            "utf8"
        )
        omp_path = os.path.join(output.rstrip(), omp_name)
        if os.path.isfile(omp_path):
            os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
            cdll.LoadLibrary(omp_path)
    except subprocess.SubprocessError:
        pass

