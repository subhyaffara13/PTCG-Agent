
def _get_metadata_or_catch_error(
    *,
    repo_id: str,
    filename: str,
    repo_type: str,
    revision: str,
    endpoint: str | None,
    etag_timeout: float | None,
    headers: dict[str, str],  # mutated inplace!
    token: bool | str | None,
    local_files_only: bool,
    relative_filename: str | None = None,  # only used to store `.no_exists` in cache
    storage_folder: str | None = None,  # only used to store `.no_exists` in cache
    retry_on_errors: bool = False,
) -> (
    # Either an exception is caught and returned
    tuple[None, None, None, None, None, Exception]
    |
    # Or the metadata is returned as
    # `(url_to_download, etag, commit_hash, expected_size, xet_file_data, None)`
    tuple[str, str, str, int, XetFileData | None, None]
):
    """Get metadata for a file on the Hub, safely handling network issues.

    Returns either the etag, commit_hash and expected size of the file, or the error
    raised while fetching the metadata.

    NOTE: This function mutates `headers` inplace! It removes the `authorization` header
          if the file is a LFS blob and the domain of the url is different from the
          domain of the location (typically an S3 bucket).
    """
    if local_files_only:
        return (
            None,
            None,
            None,
            None,
            None,
            OfflineModeIsEnabled(
                f"Cannot access file since 'local_files_only=True' as been set. (repo_id: {repo_id}, repo_type: {repo_type}, revision: {revision}, filename: {filename})"
            ),
        )

    url = hf_hub_url(repo_id, filename, repo_type=repo_type, revision=revision, endpoint=endpoint)
    url_to_download: str = url
    etag: str | None = None
    commit_hash: str | None = None
    expected_size: int | None = None
    head_error_call: Exception | None = None
    xet_file_data: XetFileData | None = None

    # Try to get metadata from the server.
    # Do not raise yet if the file is not found or not accessible.
    if not local_files_only:
        try:
            try:
                metadata = get_hf_file_metadata(
                    url=url,
                    timeout=etag_timeout,
                    headers=headers,
                    token=token,
                    endpoint=endpoint,
                    retry_on_errors=retry_on_errors,
                )
            except RemoteEntryNotFoundError as http_error:
                if storage_folder is not None and relative_filename is not None:
                    # Cache the non-existence of the file
                    commit_hash = http_error.response.headers.get(constants.HUGGINGFACE_HEADER_X_REPO_COMMIT)
                    if commit_hash is not None:
                        no_exist_file_path = Path(storage_folder) / ".no_exist" / commit_hash / relative_filename
                        if not no_exist_file_path.exists():
                            try:
                                no_exist_file_path.parent.mkdir(parents=True, exist_ok=True)
                                no_exist_file_path.touch()
                            except OSError as e:
                                logger.error(
                                    f"Could not cache non-existence of file. Will ignore error and continue. Error: {e}"
                                )
                        _cache_commit_hash_for_specific_revision(storage_folder, revision, commit_hash)
                raise

            # Commit hash must exist
            commit_hash = metadata.commit_hash
            if commit_hash is None:
                raise FileMetadataError(
                    "Distant resource does not seem to be on huggingface.co. It is possible that a configuration issue"
                    " prevents you from downloading resources from https://huggingface.co. Please check your firewall"
                    " and proxy settings and make sure your SSL certificates are updated."
                )

            # Etag must exist
            # If we don't have any of those, raise an error.
            etag = metadata.etag
            if etag is None:
                raise FileMetadataError(
                    "Distant resource does not have an ETag, we won't be able to reliably ensure reproducibility."
                )

            # Size must exist
            expected_size = metadata.size
            if expected_size is None:
                raise FileMetadataError("Distant resource does not have a Content-Length.")

            xet_file_data = metadata.xet_file_data

            # In case of a redirect, save an extra redirect on the request.get call,
            # and ensure we download the exact atomic version even if it changed
            # between the HEAD and the GET (unlikely, but hey).
            #
            # If url domain is different => we are downloading from a CDN => url is signed => don't send auth
            # If url domain is the same => redirect due to repo rename AND downloading a regular file => keep auth
            if xet_file_data is None and url != metadata.location:
                url_to_download = metadata.location
                if urlparse(url).netloc != urlparse(metadata.location).netloc:
                    # Remove authorization header when downloading a LFS blob
                    headers.pop("authorization", None)
        except httpx.ProxyError:
            # Actually raise on proxy error
            raise
        except (httpx.ConnectError, httpx.TimeoutException, OfflineModeIsEnabled) as error:
            # Otherwise, our Internet connection is down.
            # etag is None
            head_error_call = error
        except (RevisionNotFoundError, RemoteEntryNotFoundError):
            # The repo was found but the revision or entry doesn't exist on the Hub (never existed or got deleted)
            raise
        except HfHubHTTPError as error:
            # Multiple reasons for an http error:
            # - Repository is private and invalid/missing token sent
            # - Repository is gated and invalid/missing token sent
            # - Hub is down (error 500 or 504)
            # => let's switch to 'local_files_only=True' to check if the files are already cached.
            #    (if it's not the case, the error will be re-raised)
            head_error_call = error
        except FileMetadataError as error:
            # Multiple reasons for a FileMetadataError:
            # - Wrong network configuration (proxy, firewall, SSL certificates)
            # - Inconsistency on the Hub
            # => let's switch to 'local_files_only=True' to check if the files are already cached.
            #    (if it's not the case, the error will be re-raised)
            head_error_call = error

    if not (local_files_only or etag is not None or head_error_call is not None):
        raise RuntimeError("etag is empty due to uncovered problems")

    return (url_to_download, etag, commit_hash, expected_size, xet_file_data, head_error_call)  # type: ignore

