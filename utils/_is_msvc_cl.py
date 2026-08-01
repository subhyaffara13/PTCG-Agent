
def _is_msvc_cl(cpp_compiler: str) -> bool:
    if not _IS_WINDOWS:
        return False

    try:
        output_msg = (
            subprocess.check_output([cpp_compiler, "/help"], stderr=subprocess.STDOUT)
            .strip()
            .decode(*SUBPROCESS_DECODE_ARGS)
        )
        return "Microsoft" in output_msg.splitlines()[0]
    except FileNotFoundError:
        return False

    # pyrefly: ignore [unreachable]
    return False

