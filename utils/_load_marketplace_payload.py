
def _load_marketplace_payload(api) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_path = Path(tmp_dir) / "marketplace.json"
        api.download_bucket_files(
            DEFAULT_SKILLS_BUCKET_ID,
            [(MARKETPLACE_PATH, local_path)],
            raise_on_missing_files=True,
        )
        parsed = json.loads(local_path.read_text(encoding="utf-8"))

    if not isinstance(parsed, dict):
        raise CLIError("Invalid marketplace payload: expected a JSON object.")
    return parsed

