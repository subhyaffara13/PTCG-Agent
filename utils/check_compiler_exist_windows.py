import subprocess

def check_compiler_exist_windows(compiler: str) -> None:
    """
    Check if compiler is ready, in case end user not activate MSVC environment.
    """
    try:
        subprocess.check_output([compiler, "/help"], stderr=subprocess.STDOUT)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Compiler: {compiler} is not found.") from exc
    except subprocess.SubprocessError:
        # Expected that some compiler(clang, clang++) is exist, but they not support `/help` args.
        pass

