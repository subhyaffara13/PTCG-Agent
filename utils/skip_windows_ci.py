
def skip_windows_ci(name: str, file: str) -> None:
    if IS_WINDOWS and IS_CI:
        module = os.path.basename(file).strip(".py")
        sys.stderr.write(
            f"Windows CI does not have necessary dependencies for {module} tests yet\n"
        )
        if name == "__main__":
            sys.exit(0)
        raise unittest.SkipTest("requires sympy/functorch/filelock")

