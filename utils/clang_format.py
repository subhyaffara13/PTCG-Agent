
def clang_format(cpp_file_path: str) -> None:
    import subprocess

    subprocess.check_call(["clang-format", "-i", cpp_file_path])

