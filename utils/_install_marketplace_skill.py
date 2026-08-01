
def _install_marketplace_skill(api, skill: MarketplaceSkill, destination_root: Path, force: bool = False) -> Path:
    """Install a marketplace skill into a local skills directory."""
    destination_root = destination_root.expanduser().resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    install_dir = destination_root / skill.name
    already_exists = install_dir.exists()

    if already_exists and not force:
        raise FileExistsError(f"Skill already exists: {install_dir}")

    if already_exists:
        # Stage the new content in a sibling tempdir and atomically rename, so the
        # existing install stays intact if the download fails halfway through.
        with tempfile.TemporaryDirectory(dir=destination_root, prefix=f".{install_dir.name}.install-") as tmp_dir_str:
            staged_dir = Path(tmp_dir_str) / install_dir.name
            _populate_install_dir(api, skill=skill, install_dir=staged_dir)
            _atomic_replace_directory(existing_dir=install_dir, staged_dir=staged_dir)
        return install_dir

    try:
        _populate_install_dir(api, skill=skill, install_dir=install_dir)
    except Exception:
        if install_dir.exists():
            shutil.rmtree(install_dir)
        raise
    return install_dir

