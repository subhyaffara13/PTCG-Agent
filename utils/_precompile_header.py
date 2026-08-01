
def _precompile_header(
    header: str,
    hashable_cmd_line: str,
    **compile_command: Any,
) -> str:
    assert not _IS_WINDOWS, (
        "CppBuilder does not currently support precompiling on Windows!"
    )

    # Get the preprocessed output from the header file to be precompiled.  This allows
    # us to properly invalidate the file cache when any header dependency changes.  This
    # is thread-safe, as each thread will get its own temporary directory.
    #
    # N.B. we can't use NamedTemporaryFile here because Windows errors out on attempts
    # to read from a file with an open write handle.
    with tempfile.TemporaryDirectory() as preprocessing_dir:
        preprocessing_header = Path(preprocessing_dir) / "header.hpp"
        preprocessing_header.write_text(f"#include <{header}>\n")
        preprocessor = CppBuilder(
            name=str(preprocessing_header)[:-4],  # strip off the .hpp extension
            sources=str(preprocessing_header),
            BuildOption=CppTorchDeviceOptions(**compile_command, preprocessing=True),
        )
        preprocessor.build()

        def _get_file_checksum(filename: str) -> str:
            """Reading the whole preprocessed header in for hashing is very expensive,
            but calling a fast hashing utility in a subprocess is cheap."""
            # If Windows support needs to be added here, use certutil -hashfile.
            cmd_output = subprocess.run(
                ("openssl", "sha512", filename), capture_output=True, text=True
            )
            return cmd_output.stdout.split()[-1]

        preprocessor_hash = _get_file_checksum(preprocessor.get_target_file_path())

    header_build_option = CppTorchDeviceOptions(**compile_command, precompiling=True)
    header_hash, header_full_path = write(
        content=f"#include <{header}>\n",
        extension="h",
        extra=(
            hashable_cmd_line
            + preprocessor_hash
            + get_compiler_version_info(header_build_option.get_compiler())
        ),
        specified_dir=_HEADER_DIR,
    )
    cpp_builder = CppBuilder(
        name=header_full_path,
        sources=header_full_path,
        BuildOption=header_build_option,
    )
    # _worker_compile_cpp will automatically ignore any compilation whose result already
    # exists, so this is always safe.
    os.makedirs(_HEADER_LOCK_DIR, exist_ok=True)
    _worker_compile_cpp(
        os.path.join(_HEADER_LOCK_DIR, f"{header_hash}.lock"),
        (cpp_builder,),
    )

    return header_full_path

