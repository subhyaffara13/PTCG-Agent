from pathlib import Path


def cuda_standalone_runner_compile_command(srcpath: Path, exepath: Path):
    # returns command string to compile a (captured) CUDA GEMM Kernel source to a standalone executable that's ready to run
    # Passes the correct preprocessor define to nvcc to ensure the standalone runner is enabled.

    extra_args = ["-DGENERATE_STANDALONE_RUNNER=1", "-DCUTLASS_DEBUG_TRACE_LEVEL=1"]
    compile_command = cuda_compile_command(
        [str(srcpath)], str(exepath), "exe", extra_args=extra_args
    )
    return compile_command

