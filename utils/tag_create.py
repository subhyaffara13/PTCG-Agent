
def tag_create(
    repo_id: RepoIdArg,
    tag: Annotated[
        str,
        typer.Argument(
            help="The name of the tag to create.",
        ),
    ],
    message: Annotated[
        str | None,
        typer.Option(
            "-m",
            "--message",
            help="The description of the tag to create.",
        ),
    ] = None,
    revision: RevisionOpt = None,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """Create a tag for a repo."""
    repo_type_str = repo_type.value
    api = get_hf_api(token=token)
    try:
        api.create_tag(repo_id=repo_id, tag=tag, tag_message=message, revision=revision, repo_type=repo_type_str)
    except RepositoryNotFoundError as e:
        raise CLIError(f"{repo_type_str.capitalize()} '{repo_id}' not found.") from e
    except RevisionNotFoundError as e:
        raise CLIError(f"Revision '{revision}' not found.") from e
    except HfHubHTTPError as e:
        if e.response.status_code == 409:
            raise CLIError(f"Tag '{tag}' already exists on '{repo_id}'.") from e
        raise
    out.result("Tag created", tag=tag, repo_type=repo_type_str, repo_id=repo_id)

