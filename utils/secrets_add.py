
def secrets_add(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    secrets: SecretsOpt = None,
    secrets_file: SecretsFileOpt = None,
    token: TokenOpt = None,
) -> None:
    """Add or update secrets for a Space."""
    secrets_map = parse_env_map(secrets, secrets_file)
    if not secrets_map:
        raise CLIError("At least one secret must be specified with -s/--secrets or --secrets-file.")
    api = get_hf_api(token=token)
    for key, value in secrets_map.items():
        api.add_space_secret(space_id, key=key, value=value or "")
    out.result("Secrets added", space_id=space_id, keys=list(secrets_map))
    out.hint(f"Use `hf spaces secrets delete {space_id} <key>` to remove a secret from a Space.")

