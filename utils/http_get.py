
def http_get(
    url: str,
    temp_file: BinaryIO,
    *,
    resume_size: int = 0,
    headers: dict[str, Any] | None = None,
    expected_size: int | None = None,
    displayed_filename: str | None = None,
    tqdm_class: type[base_tqdm] | None = None,
    _nb_retries: int = 5,
    _tqdm_bar: tqdm | None = None,
) -> None:
    """
    Download a remote file. Do not gobble up errors, and will return errors tailored to the Hugging Face Hub.

    If ConnectionError (SSLError) or ReadTimeout happen while streaming data from the server, it is most likely a
    transient error (network outage?). We log a warning message and try to resume the download a few times before
    giving up. The method gives up after 5 attempts if no new data has being received from the server.

    Args:
        url (`str`):
            The URL of the file to download.
        temp_file (`BinaryIO`):
            The file-like object where to save the file.
        resume_size (`int`, *optional*):
            The number of bytes already downloaded. If set to 0 (default), the whole file is download. If set to a
            positive number, the download will resume at the given position.
        headers (`dict`, *optional*):
            Dictionary of HTTP Headers to send with the request.
        expected_size (`int`, *optional*):
            The expected size of the file to download. If set, the download will raise an error if the size of the
            received content is different from the expected one.
        displayed_filename (`str`, *optional*):
            The filename of the file that is being downloaded. Value is used only to display a nice progress bar. If
            not set, the filename is guessed from the URL or the `Content-Disposition` header.
    """
    if expected_size is not None and resume_size == expected_size:
        # If the file is already fully downloaded, we don't need to download it again.
        return

    initial_headers = headers
    headers = copy.deepcopy(headers) or {}
    if resume_size > 0:
        headers["Range"] = _adjust_range_header(headers.get("Range"), resume_size)
    elif expected_size and expected_size > constants.MAX_HTTP_DOWNLOAD_SIZE:
        # Any files over 50GB will not be available through basic http requests.
        raise ValueError(
            "The file is too large to be downloaded using the regular download method. "
            " Install `hf_xet` with `pip install hf_xet` for xet-powered downloads."
        )

    with http_stream_backoff(
        method="GET",
        url=url,
        headers=headers,
        timeout=constants.HF_HUB_DOWNLOAD_TIMEOUT,
        retry_on_exceptions=(),
        retry_on_status_codes=(408, 429),
    ) as response:
        hf_raise_for_status(response)

        # If we requested a Range but got 200 back, the server ignored our Range header
        # (e.g. CloudFront with Accept-Encoding: gzip). Reset file to avoid corruption.
        if resume_size > 0 and response.status_code == 200:
            temp_file.seek(0)
            temp_file.truncate()
            if _tqdm_bar is not None:
                # When the progress bar is reused across retries, its counter has already been advanced by `resume_size`
                # worth of chunks from earlier attempts. Those bytes are gone from disk now, so roll the counter back
                # to keep the upcoming full re-download from double-counting (e.g. ending at 130/100 on a 100-byte file).
                _tqdm_bar.update(-resume_size)
            resume_size = 0

        total: int | None = _get_file_length_from_http_response(response)
        if total is None:
            # Hub serves compressible text files (e.g. vocab.json) with `Content-Encoding: gzip` and
            # `Transfer-Encoding: chunked`, so the response carries no `Content-Length`. Fall back to the caller's
            # `expected_size` (always known from the metadata HEAD on the hf_hub path) so the progress bar, and any
            # aggregating wrapper such as snapshot_download's `_AggregatedTqdm` — still sees the file size.
            total = expected_size

        if displayed_filename is None:
            displayed_filename = url
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition is not None:
                match = HEADER_FILENAME_PATTERN.search(content_disposition)
                if match is not None:
                    # Means file is on CDN
                    displayed_filename = match.groupdict()["filename"]

        # Truncate filename if too long to display
        if len(displayed_filename) > 40:
            displayed_filename = f"(…){displayed_filename[-40:]}"

        consistency_error_message = (
            f"Consistency check failed: file should be of size {expected_size} but has size"
            f" {{actual_size}} ({displayed_filename}).\nThis is usually due to network issues while downloading the file."
            " Please retry with `force_download=True`."
        )
        progress_cm = _get_progress_bar_context(
            desc=displayed_filename,
            log_level=logger.getEffectiveLevel(),
            total=total,
            initial=resume_size,
            name="huggingface_hub.http_get",
            tqdm_class=tqdm_class,
            _tqdm_bar=_tqdm_bar,
        )

        with progress_cm as progress:
            new_resume_size = resume_size
            try:
                for chunk in response.iter_bytes(chunk_size=constants.DOWNLOAD_CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        progress.update(len(chunk))
                        temp_file.write(chunk)
                        new_resume_size += len(chunk)
                        # Some data has been downloaded from the server so we reset the number of retries.
                        _nb_retries = 5
            except (httpx.ConnectError, httpx.TimeoutException, httpx.RemoteProtocolError) as e:
                # If ConnectionError (SSLError), ReadTimeout, or RemoteProtocolError (peer closed the connection before
                # sending the complete body) happen while streaming data from the server, it is most likely a transient
                # error (network outage?). We log a warning message and try to resume the download a few times  before
                # giving up. The retry mechanism is basic but should be enough in most cases.
                if _nb_retries <= 0:
                    logger.warning("Error while downloading from %s: %s\nMax retries exceeded.", url, str(e))
                    raise
                logger.warning("Error while downloading from %s: %s\nTrying to resume download...", url, str(e))
                time.sleep(1)
                return http_get(
                    url=url,
                    temp_file=temp_file,
                    resume_size=new_resume_size,
                    headers=initial_headers,
                    expected_size=expected_size,
                    tqdm_class=tqdm_class,
                    _nb_retries=_nb_retries - 1,
                    # Reuse the existing progress bar across retries so a custom `tqdm_class` (e.g. snapshot_download's `_AggregatedTqdm`,
                    # which mutates a shared parent bar in `__init__`) is not re-instantiated and does not double-count `total`/`initial`.
                    _tqdm_bar=progress,
                )

    if expected_size is not None and expected_size != temp_file.tell():
        raise OSError(
            consistency_error_message.format(
                actual_size=temp_file.tell(),
            )
        )

