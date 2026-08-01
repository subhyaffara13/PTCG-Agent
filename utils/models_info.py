
def models_info(
    model_id: Annotated[str, typer.Argument(help="The model ID (e.g. `username/repo-name`).")],
    revision: RevisionOpt = None,
    expand: ExpandOpt = None,
    token: TokenOpt = None,
) -> None:
    """Get info about a model on the Hub."""
    api = get_hf_api(token=token)
    try:
        info = api.model_info(repo_id=model_id, revision=revision, expand=expand)  # type: ignore
    except RepositoryNotFoundError as e:
        raise CLIError(f"Model '{model_id}' not found.") from e
    except RevisionNotFoundError as e:
        raise CLIError(f"Revision '{revision}' not found on '{model_id}'.") from e
    out.dict(info)

