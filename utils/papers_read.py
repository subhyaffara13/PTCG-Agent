
def papers_read(
    paper_id: Annotated[str, typer.Argument(help="The arXiv paper ID (e.g. '2502.08025').")],
    token: TokenOpt = None,
) -> None:
    """Read a paper as markdown."""
    api = get_hf_api(token=token)
    try:
        content = api.read_paper(id=paper_id)
    except HfHubHTTPError as e:
        if e.response.status_code == 404:
            raise CLIError(f"Paper '{paper_id}' not found on the Hub.") from e
        raise
    out.text(content)

