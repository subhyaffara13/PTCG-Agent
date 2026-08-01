
def list_catalog(
    token: TokenOpt = None,
) -> None:
    """List available Catalog models."""
    api = get_hf_api(token=token)
    try:
        models = api.list_inference_catalog(token=token)
    except HfHubHTTPError as error:
        out.error(f"Catalog fetch failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error

    out.dict({"models": models})

