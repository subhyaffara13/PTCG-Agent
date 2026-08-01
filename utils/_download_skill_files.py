
def _download_skill_files(api, skill: MarketplaceSkill, files: list[BucketFile], install_dir: Path) -> None:
    """Download bucket files into `install_dir`."""
    prefix = skill.repo_path.rstrip("/")
    prefix_with_slash = f"{prefix}/"

    # `list_bucket_tree(prefix=...)` matches as a raw string prefix, so e.g. asking for
    # "skills/gradio" can also return "skills/gradio-tools/...". Filter on the trailing
    # slash to keep only files actually inside the directory, then strip it so files land
    # directly under `install_dir` preserving any nested structure.
    download_specs: list[tuple[str | BucketFile, str | Path]] = []
    for bucket_file in files:
        if not bucket_file.path.startswith(prefix_with_slash):
            continue
        relative = bucket_file.path[len(prefix_with_slash) :]
        local_file = install_dir.joinpath(*PurePosixPath(relative).parts)
        local_file.parent.mkdir(parents=True, exist_ok=True)
        download_specs.append((bucket_file, local_file))

    if not download_specs:
        raise FileNotFoundError(f"No files found under '{prefix}' in bucket '{DEFAULT_SKILLS_BUCKET_ID}'.")

    api.download_bucket_files(DEFAULT_SKILLS_BUCKET_ID, download_specs)

