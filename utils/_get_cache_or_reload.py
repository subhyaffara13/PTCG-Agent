import os
import sys

def _get_cache_or_reload(
    github,
    force_reload,
    trust_repo,
    verbose=True,
    skip_validation=False,
):
    # Setup hub_dir to save downloaded files
    hub_dir = get_dir()
    os.makedirs(hub_dir, exist_ok=True)
    # Parse github repo information
    repo_owner, repo_name, ref = _parse_repo_info(github)
    # Github allows branch name with slash '/',
    # this causes confusion with path on both Linux and Windows.
    # Backslash is not allowed in Github branch name so no need to
    # to worry about it.
    normalized_br = ref.replace("/", "_")
    # Github renames folder repo-v1.x.x to repo-1.x.x
    # We don't know the repo name before downloading the zip file
    # and inspect name from it.
    # To check if cached repo exists, we need to normalize folder names.
    owner_name_branch = "_".join([repo_owner, repo_name, normalized_br])
    repo_dir = os.path.join(hub_dir, owner_name_branch)
    # Check that the repo is in the trusted list
    _check_repo_is_trusted(
        repo_owner,
        repo_name,
        owner_name_branch,
        trust_repo=trust_repo,
    )

    use_cache = (not force_reload) and os.path.exists(repo_dir)

    if use_cache:
        if verbose:
            sys.stderr.write(f"Using cache found in {repo_dir}\n")
    else:
        # Validate the tag/branch is from the original repo instead of a forked repo
        if not skip_validation:
            _validate_not_a_forked_repo(repo_owner, repo_name, ref)

        cached_file = os.path.join(hub_dir, normalized_br + ".zip")
        _remove_if_exists(cached_file)

        try:
            url = _git_archive_link(repo_owner, repo_name, ref)
            sys.stdout.write(f'Downloading: "{url}" to {cached_file}\n')
            download_url_to_file(url, cached_file, progress=False)
        except HTTPError as err:
            if err.code == 300:
                # Getting a 300 Multiple Choices error likely means that the ref is both a tag and a branch
                # in the repo. This can be disambiguated by explicitly using refs/heads/ or refs/tags
                # See https://git-scm.com/book/en/v2/Git-Internals-Git-References
                # Here, we do the same as git: we throw a warning, and assume the user wanted the branch
                warnings.warn(
                    f"The ref {ref} is ambiguous. Perhaps it is both a tag and a branch in the repo? "
                    "Torchhub will now assume that it's a branch. "
                    "You can disambiguate tags and branches by explicitly passing refs/heads/branch_name or "
                    "refs/tags/tag_name as the ref. That might require using skip_validation=True.",
                    stacklevel=2,
                )
                disambiguated_branch_ref = f"refs/heads/{ref}"
                url = _git_archive_link(
                    repo_owner, repo_name, ref=disambiguated_branch_ref
                )
                download_url_to_file(url, cached_file, progress=False)
            else:
                raise

        with zipfile.ZipFile(cached_file) as cached_zipfile:
            extraced_repo_name = cached_zipfile.infolist()[0].filename
            extracted_repo = os.path.join(hub_dir, extraced_repo_name)
            _remove_if_exists(extracted_repo)
            # Unzip the code and rename the base folder using safe extraction
            _safe_extract_zip(cached_zipfile, hub_dir)

        _remove_if_exists(cached_file)
        _remove_if_exists(repo_dir)
        shutil.move(extracted_repo, repo_dir)  # rename the repo

    return repo_dir

