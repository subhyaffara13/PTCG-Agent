
def _load_policy_templates_from_local_backup() -> list:
    """Load policy templates from local backup file (litellm/policy_templates_backup.json)."""
    backup_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
        "policy_templates_backup.json",
    )
    path = os.path.abspath(backup_path)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

