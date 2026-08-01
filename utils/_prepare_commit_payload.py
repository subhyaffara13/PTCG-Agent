
def _prepare_commit_payload(
    operations: Iterable[CommitOperation],
    files_to_copy: dict[_CopySource, Union["RepoFile", bytes]],
    commit_message: str,
    commit_description: str | None = None,
    parent_commit: str | None = None,
) -> Iterable[dict[str, Any]]:
    """
    Builds the payload to POST to the `/commit` API of the Hub.

    Payload is returned as an iterator so that it can be streamed as a ndjson in the
    POST request.

    For more information, see:
        - https://github.com/huggingface/huggingface_hub/issues/1085#issuecomment-1265208073
        - http://ndjson.org/
    """
    commit_description = commit_description if commit_description is not None else ""

    # 1. Send a header item with the commit metadata
    header_value = {"summary": commit_message, "description": commit_description}
    if parent_commit is not None:
        header_value["parentCommit"] = parent_commit
    yield {"key": "header", "value": header_value}

    nb_ignored_files = 0

    # 2. Send operations, one per line
    for operation in operations:
        # Skip ignored files
        if isinstance(operation, CommitOperationAdd) and operation._should_ignore:
            logger.debug(f"Skipping file '{operation.path_in_repo}' in commit (ignored by gitignore file).")
            nb_ignored_files += 1
            continue

        # 2.a. Case adding a regular file
        if isinstance(operation, CommitOperationAdd) and operation._upload_mode == "regular":
            yield {
                "key": "file",
                "value": {
                    "content": operation.b64content().decode(),
                    "path": operation.path_in_repo,
                    "encoding": "base64",
                },
            }
        # 2.b. Case adding an LFS file
        elif isinstance(operation, CommitOperationAdd) and operation._upload_mode == "lfs":
            yield {
                "key": "lfsFile",
                "value": {
                    "path": operation.path_in_repo,
                    "algo": "sha256",
                    "oid": operation.upload_info.sha256.hex(),
                    "size": operation.upload_info.size,
                },
            }
        # 2.c. Case deleting a file or folder
        elif isinstance(operation, CommitOperationDelete):
            yield {
                "key": "deletedFolder" if operation.is_folder else "deletedFile",
                "value": {"path": operation.path_in_repo},
            }
        # 2.d. Case copying a file or folder
        elif isinstance(operation, CommitOperationCopy):
            source = _CopySource(
                operation.src_repo_id,
                operation.src_repo_type,
                operation.src_path_in_repo,
                operation.src_revision,
            )
            file_to_copy = files_to_copy[source]
            if isinstance(file_to_copy, bytes):
                yield {
                    "key": "file",
                    "value": {
                        "content": base64.b64encode(file_to_copy).decode(),
                        "path": operation.path_in_repo,
                        "encoding": "base64",
                    },
                }
            elif file_to_copy.lfs:
                yield {
                    "key": "lfsFile",
                    "value": {
                        "path": operation.path_in_repo,
                        "algo": "sha256",
                        "oid": file_to_copy.lfs.sha256,
                    },
                }
            else:
                raise ValueError(
                    "Malformed files_to_copy (should be raw file content as bytes or RepoFile objects with LFS info."
                )
        # 2.e. Never expected to happen
        else:
            raise ValueError(
                f"Unknown operation to commit. Operation: {operation}. Upload mode:"
                f" {getattr(operation, '_upload_mode', None)}"
            )

    if nb_ignored_files > 0:
        logger.info(f"Skipped {nb_ignored_files} file(s) in commit (ignored by gitignore file).")

