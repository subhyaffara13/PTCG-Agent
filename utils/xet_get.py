
def xet_get(
    *,
    incomplete_path: Path,
    xet_file_data: XetFileData,
    headers: dict[str, str],
    expected_size: int | None = None,
    displayed_filename: str | None = None,
    tqdm_class: type[base_tqdm] | None = None,
    _tqdm_bar: tqdm | None = None,
) -> None:
    """
    Download a file using Xet storage service.

    Args:
        incomplete_path (`Path`):
            The path to the file to download.
        xet_file_data (`XetFileData`):
            The file metadata needed to make the request to the xet storage service.
        headers (`dict[str, str]`):
            The headers to send to the xet storage service.
        expected_size (`int`, *optional*):
            The expected size of the file to download. If set, the download will raise an error if the size of the
            received content is different from the expected one.
        displayed_filename (`str`, *optional*):
            The filename of the file that is being downloaded. Value is used only to display a nice progress bar. If
            not set, the filename is guessed from the URL or the `Content-Disposition` header.

    **How it works:**
        The file download system uses Xet storage, which is a content-addressable storage system that breaks files into chunks
        for efficient storage and transfer.

        ``session.new_file_download_group()`` manages downloading files by:
        - Registering download tasks (each with its unique content hash) and starting download immediately in the background
        - Connecting to a storage server (CAS server) that knows how files are chunked
        - Using authentication to ensure secure access
        - Providing progress updates during download

        Authentication works transparently: the download group accepts a ``token_refresh_url``
        that is used to refresh the short-lived xet access token as needed.

        The download process works like this:
        1. Download tasks run in parallel:
            1.1. Prepare to write the file to disk or to a stream (e.g. truncate file, set up cache)
            1.2. Ask the server "how is this file split into chunks?" using the file's unique hash
                The server responds with:
                - Which chunks make up the complete file
                - Where each chunk can be downloaded from
            1.3. For each needed chunk:
                - Checks if we already have it in our local cache
                - If not, download it from cloud storage (S3)
                - Save it to cache for future use
                - Assemble the chunks in order to recreate the original file

    """
    try:
        from hf_xet import XetFileInfo  # type: ignore[no-redef]
    except ImportError:
        raise ValueError(
            "To use optimized download using Xet storage, you need to install the hf_xet package. "
            'Try `pip install "huggingface_hub[hf_xet]"` or `pip install hf_xet`.'
        )

    if not displayed_filename:
        displayed_filename = incomplete_path.name

    # Truncate filename if too long to display
    if len(displayed_filename) > 40:
        displayed_filename = f"{displayed_filename[:40]}(…)"

    progress_cm = _get_progress_bar_context(
        desc=displayed_filename,
        log_level=logger.getEffectiveLevel(),
        total=expected_size,
        initial=0,
        name="huggingface_hub.xet_get",
        tqdm_class=tqdm_class,
        _tqdm_bar=_tqdm_bar,
    )

    from .utils._xet import abort_xet_session, get_xet_session, xet_headers_without_auth

    xet_headers = xet_headers_without_auth(headers)

    session = get_xet_session()

    with progress_cm as progress:
        _prev = 0

        def _on_progress(group_report, _):
            nonlocal _prev
            current = group_report.total_bytes_completed
            progress.update(max(0, current - _prev))
            _prev = current

        try:
            with session.new_file_download_group(
                token_refresh_url=xet_file_data.refresh_route,
                token_refresh_headers=headers,
                custom_headers=xet_headers,
                progress_callback=_on_progress,
            ) as group:
                group.start_download_file(
                    XetFileInfo(xet_file_data.file_hash, expected_size), str(incomplete_path.absolute())
                )
        except KeyboardInterrupt:
            abort_xet_session()
            raise

