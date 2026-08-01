
def variables_add(
    space_id: Annotated[str, typer.Argument(help="The space ID (e.g. `username/repo-name`).")],
    env: EnvOpt = None,
    env_file: EnvFileOpt = None,
    token: TokenOpt = None,
) -> None:
    """Add or update environment variables for a Space."""
    env_map = parse_env_map(env, env_file)
    if not env_map:
        raise CLIError("At least one variable must be specified with -e/--env or --env-file.")
    api = get_hf_api(token=token)
    for key, value in env_map.items():
        api.add_space_variable(space_id, key=key, value=value or "")
    out.result("Variables added", space_id=space_id, keys=list(env_map))
    out.hint(f"Use `hf spaces variables ls {space_id}` to list variables for a Space.")

