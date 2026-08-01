
def hf_raise_for_status(response: httpx.Response, endpoint_name: str | None = None) -> None:
    """
    Internal version of `response.raise_for_status()` that will refine a potential HTTPError.
    Raised exception will be an instance of [`~errors.HfHubHTTPError`].

    This helper is meant to be the unique method to raise_for_status when making a call to the Hugging Face Hub.

    Args:
        response (`Response`):
            Response from the server.
        endpoint_name (`str`, *optional*):
            Name of the endpoint that has been called. If provided, the error message will be more complete.

    > [!WARNING]
    > Raises when the request has failed:
    >
    >     - [`~utils.RepositoryNotFoundError`]
    >         If the repository to download from cannot be found. This may be because it
    >         doesn't exist, because `repo_type` is not set correctly, or because the repo
    >         is `private` and you do not have access.
    >     - [`~utils.GatedRepoError`]
    >         If the repository exists but is gated and the user is not on the authorized
    >         list.
    >     - [`~utils.RevisionNotFoundError`]
    >         If the repository exists but the revision couldn't be found.
    >     - [`~utils.EntryNotFoundError`]
    >         If the repository exists but the entry (e.g. the requested file) couldn't be
    >         find.
    >     - [`~utils.BadRequestError`]
    >         If request failed with a HTTP 400 BadRequest error.
    >     - [`~utils.HfHubHTTPError`]
    >         If request failed for a reason not listed above.
    """
    try:
        _warn_on_warning_headers(response)
    except Exception:
        # Never raise on warning parsing
        logger.debug("Failed to parse warning headers", exc_info=True)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if response.status_code // 100 == 3:
            return  # Do not raise on redirects to stay consistent with `requests`

        error_code = response.headers.get("X-Error-Code")
        error_message = response.headers.get("X-Error-Message")

        # Parse repo info from request URL (used to enrich errors below)
        request_url = (
            str(response.request.url) if response.request is not None and response.request.url is not None else None
        )
        repo_type, repo_id = _parse_repo_info_from_url(request_url) if request_url else (None, None)

        if error_code == "RevisionNotFound":
            message = f"{response.status_code} Client Error." + "\n\n" + f"Revision Not Found for url: {response.url}."
            raise _format(RevisionNotFoundError, message, response, repo_type=repo_type, repo_id=repo_id) from e

        elif error_code == "EntryNotFound":
            message = f"{response.status_code} Client Error." + "\n\n" + f"Entry Not Found for url: {response.url}."
            raise _format(RemoteEntryNotFoundError, message, response, repo_type=repo_type, repo_id=repo_id) from e

        elif error_code == "GatedRepo":
            message = (
                f"{response.status_code} Client Error." + "\n\n" + f"Cannot access gated repo for url {response.url}."
            )
            raise _format(GatedRepoError, message, response, repo_type=repo_type, repo_id=repo_id) from e

        elif error_message == "Access to this resource is disabled.":
            message = (
                f"{response.status_code} Client Error."
                + "\n\n"
                + f"Cannot access repository for url {response.url}."
                + "\n"
                + "Access to this resource is disabled."
            )
            raise _format(DisabledRepoError, message, response) from e

        elif (
            error_code == "RepoNotFound"
            and request_url is not None
            and BUCKET_API_REGEX.search(request_url) is not None
        ):
            message = (
                f"{response.status_code} Client Error."
                + "\n\n"
                + f"Bucket Not Found for url: {response.url}."
                + "\nPlease make sure you specified the correct bucket id (namespace/name)."
                + "\nIf the bucket is private, make sure you are authenticated and your token has the required permissions."
            )
            raise _format(
                BucketNotFoundError, message, response, bucket_id=_parse_bucket_id_from_url(request_url)
            ) from e

        elif (
            response.status_code == 404
            and request_url is not None
            and (job_id := _parse_job_id_from_url(request_url)) is not None
        ):
            message = (
                f"{response.status_code} Client Error."
                + "\n\n"
                + f"Job Not Found for url: {response.url}."
                + "\nPlease make sure you specified the correct job ID and namespace."
            )
            raise _format(JobNotFoundError, message, response, job_id=job_id) from e

        elif error_code == "RepoNotFound" or (
            response.status_code == 401
            and error_message != "Invalid credentials in Authorization header"
            and request_url is not None
            and REPO_API_REGEX.search(request_url) is not None
        ):
            # 401 is misleading as it is returned for:
            #    - private and gated repos if user is not authenticated
            #    - missing repos
            # => for now, we process them as `RepoNotFound` anyway.
            # See https://gist.github.com/Wauplin/46c27ad266b15998ce56a6603796f0b9
            message = (
                f"{response.status_code} Client Error."
                + "\n\n"
                + f"Repository Not Found for url: {response.url}."
                + "\nPlease make sure you specified the correct `repo_id` and"
                " `repo_type`.\nIf you are trying to access a private or gated repo,"
                " make sure you are authenticated and your token has the required permissions."
                + "\nFor more details, see https://huggingface.co/docs/huggingface_hub/authentication"
            )
            raise _format(RepositoryNotFoundError, message, response, repo_type=repo_type, repo_id=repo_id) from e

        elif response.status_code == 400:
            message = (
                f"\n\nBad request for {endpoint_name} endpoint:" if endpoint_name is not None else "\n\nBad request:"
            )
            raise _format(BadRequestError, message, response) from e

        elif response.status_code == 403:
            message = (
                f"\n\n{response.status_code} Forbidden: {error_message}."
                + f"\nCannot access content at: {response.url}."
                + "\nMake sure your token has the correct permissions."
            )
            raise _format(HfHubHTTPError, message, response) from e

        elif response.status_code == 429:
            ratelimit_info = parse_ratelimit_headers(response.headers)
            if ratelimit_info is not None:
                message = (
                    f"\n\n429 Too Many Requests: you have reached your '{ratelimit_info.resource_type}' rate limit."
                )
                message += f"\nRetry after {ratelimit_info.reset_in_seconds} seconds"
                if ratelimit_info.limit is not None and ratelimit_info.window_seconds is not None:
                    message += (
                        f" ({ratelimit_info.remaining}/{ratelimit_info.limit} requests remaining"
                        f" in current {ratelimit_info.window_seconds}s window)."
                    )
                else:
                    message += "."
                message += f"\nUrl: {response.url}."
            else:
                message = f"\n\n429 Too Many Requests for url: {response.url}."
            raise _format(HfHubHTTPError, message, response) from e

        elif response.status_code == 416:
            range_header = response.request.headers.get("Range")
            message = f"{e}. Requested range: {range_header}. Content-Range: {response.headers.get('Content-Range')}."
            raise _format(HfHubHTTPError, message, response) from e

        # Convert `HTTPError` into a `HfHubHTTPError` to display request information
        # as well (request id and/or server error message)
        raise _format(HfHubHTTPError, str(e), response) from e

