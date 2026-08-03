from typing import Any
from pathlib import Path


def check_file(
    filename: str | Path,
    show_diff: bool | TextIO = False,
    config: Config = DEFAULT_CONFIG,
    file_path: Path | None = None,
    disregard_skip: bool = True,
    extension: str | None = None,
    **config_kwargs: Any,
) -> bool:
    """Checks any imports within the provided file, returning `False` if any unsorted or
    incorrectly imports are found or `True` if no problems are identified.

    - **filename**: The name or Path of the file to check.
    - **show_diff**: If `True` the changes that need to be done will be printed to stdout, if a
    TextIO stream is provided results will be written to it, otherwise no diff will be computed.
    - **config**: The config object to use when sorting imports.
    - **file_path**: The disk location where the code string was pulled from.
    - **disregard_skip**: set to `True` if you want to ignore a skip set in config for this file.
    - **extension**: The file extension that contains imports. Defaults to filename extension or py.
    - ****config_kwargs**: Any config modifications.
    """
    file_config: Config = config

    if "config_trie" in config_kwargs:
        config_trie = config_kwargs.pop("config_trie", None)
        if config_trie:
            config_info = config_trie.search(filename)
            if config.verbose:
                print(f"{config_info[0]} used for file {filename}")

            file_config = Config(**config_info[1])

    with io.File.read(filename) as source_file:
        return check_stream(
            source_file.stream,
            show_diff=show_diff,
            extension=extension,
            config=file_config,
            file_path=file_path or source_file.path,
            disregard_skip=disregard_skip,
            **config_kwargs,
        )


def check_file(filename: str | None, is_inlined_call: bool = False) -> SkipResult:
    """Should skip this file?"""
    if filename is None:
        return SkipResult(
            True, "cannot determine source file (likely a C extension or builtin)"
        )
    filename = _as_posix_path(filename)
    if filename in FORCE_SKIP_FILES:
        return SkipResult(True, f"file is force-skipped ({filename})")

    for d in get_legacy_mod_inlinelist():
        if filename.startswith(d):
            return SkipResult(False, f"file matches LEGACY_MOD_INLINELIST ({d})")
    if is_inlined_call and is_torch_inline_allowed(filename):
        return SkipResult(False, f"file matches MOD_INLINELIST ({filename})")
    if is_inlined_call and any(
        filename.startswith(d) for d in BUILTIN_INLINE_WHEN_CALLED
    ):
        return SkipResult(
            False, f"file matches BUILTIN_INLINE_WHEN_CALLED ({filename})"
        )
    if (
        is_fbcode()
        and FBCODE_SKIP_DIRS
        and bool(FBCODE_SKIP_DIRS_RE.match(filename))
        and not bool(FBCODE_INLINE_FILES_IN_SKIPPED_DIRS_RE.match(filename))
    ):
        return SkipResult(True, "file matches FBCODE_SKIP_DIRS")

    if (
        is_fbcode()
        and config.skip_torchrec
        and FBCODE_SKIP_TORCHREC_DIRS
        and bool(FBCODE_SKIP_TORCHREC_DIRS_RE.match(filename))
        and not bool(FBCODE_INLINE_FILES_IN_SKIPPED_DIRS_RE.match(filename))
    ):
        return SkipResult(True, "file matches FBCODE_SKIP_TORCHREC_DIRS")

    unittest_dir = _module_dir(unittest)
    if (
        unittest_dir is not None
        and filename.startswith(unittest_dir)
        and not torch._dynamo.config.enable_trace_unittest
    ):
        return SkipResult(True, "file is in unittest directory")

    if bool(SKIP_DIRS_RE.match(filename)):
        matched_dir = next((d for d in SKIP_DIRS if filename.startswith(d)), filename)
        return SkipResult(True, f"file is under skip directory ({matched_dir})")

    for d in get_mod_skiplist():
        if filename.startswith(d):
            return SkipResult(True, f"file matches MOD_SKIPLIST ({d})")
    return SkipResult(False, "inlined by default")


def check_file(filename):
    """Checks a file for CUDA kernel launches without cuda error checks

    Args:
        filename - File to check

    Returns:
        The number of unsafe kernel launches in the file
    """
    if not (filename.endswith((".cu", ".cuh"))):
        return 0
    if should_exclude_file(filename):
        return 0
    with open(filename) as f:
        contents = f.read()
        unsafeCount = check_code_for_cuda_kernel_launches(contents, filename)
    return unsafeCount

