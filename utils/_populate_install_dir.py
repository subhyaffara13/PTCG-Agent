
def _populate_install_dir(api, skill: MarketplaceSkill, install_dir: Path) -> None:
    install_dir.mkdir(parents=True, exist_ok=True)
    bucket_files = _list_skill_files(api, skill)
    _download_skill_files(api, skill, bucket_files, install_dir)
    _validate_installed_skill_dir(install_dir)
    (install_dir / MANAGED_MARKER_FILENAME).touch()

