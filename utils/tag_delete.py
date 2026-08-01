
def tag_delete(
    repo_id: RepoIdArg,
    tag: Annotated[
        str,
        typer.Argument(
            help="The name of the tag to delete.",
        ),
    ],
    yes: Annotated[
        bool,
        typer.Option(
            "-y",
            "--yes",
            help="Answer Yes to prompt automatically",
        ),
    ] = False,
    token: TokenOpt = None,
    repo_type: RepoTypeOpt = RepoType.model,
) -> None:
    """Delete a tag for a repo."""
    repo_type_str = repo_type.value
    out.text(f"You are about to delete tag {tag} on {repo_type_str} {repo_id}")
    out.confirm("Proceed?", yes=yes)
    api = get_hf_api(token=token)
    try:
        api.delete_tag(repo_id=repo_id, tag=tag, repo_type=repo_type_str)
    except RepositoryNotFoundError as e:
        raise CLIError(f"{repo_type_str.capitalize()} '{repo_id}' not found.") from e
    except RevisionNotFoundError as e:
        raise CLIError(f"Tag '{tag}' not found on '{repo_id}'.") from e
    out.result("Tag deleted", tag=tag, repo_type=repo_type_str, repo_id=repo_id)

