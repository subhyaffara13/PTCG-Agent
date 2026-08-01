
def _is_intel_compiler(cpp_compiler: str) -> bool:
    def _check_minimal_version(compiler_version: TorchVersion) -> None:
        """
        On Windows: early version icx has `-print-file-name` issue, and can't preload correctly for inductor.
        """
        min_version = "2024.2.1" if _IS_WINDOWS else "0.0.0"
        if compiler_version < TorchVersion(min_version):
            raise RuntimeError(
                f"Intel Compiler error: less than minimal version {min_version}."
            )

    try:
        output_msg = (
            subprocess.check_output(
                [cpp_compiler, "--version"], stderr=subprocess.DEVNULL
            )
            .strip()
            .decode(*SUBPROCESS_DECODE_ARGS)
        )
        is_intel_compiler = "Intel" in output_msg.splitlines()[0]
        if is_intel_compiler:
            if _IS_WINDOWS:
                if re.search(r"((icx$)|(icx-cc$))", cpp_compiler):
                    raise RuntimeError(
                        "Please use icx-cl, due to torch.compile only support MSVC-like CLI (compiler flags syntax)."
                    )

            # Version check
            icx_ver_search = re.search(r"(\d+[.]\d+[.]\d+[.]\d+)", output_msg)
            if icx_ver_search is not None:
                icx_ver = icx_ver_search.group(1)
                _check_minimal_version(TorchVersion(icx_ver))

        return is_intel_compiler
    except FileNotFoundError:
        return False
    except subprocess.SubprocessError:
        # --version args not support.
        return False

    # pyrefly: ignore [unreachable]
    return False

