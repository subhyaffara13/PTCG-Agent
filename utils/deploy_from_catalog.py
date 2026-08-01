
def deploy_from_catalog(
    repo: Annotated[
        str,
        typer.Option(
            help="The name of the model repository associated with the Inference Endpoint (e.g. 'openai/gpt-oss-120b').",
        ),
    ],
    name: NameOpt = None,
    accelerator: Annotated[
        str | None,
        typer.Option(
            help="The hardware accelerator to be used for inference (e.g. 'cpu', 'gpu', 'neuron').",
        ),
    ] = None,
    namespace: NamespaceOpt = None,
    token: TokenOpt = None,
) -> None:
    """Deploy an Inference Endpoint from the Model Catalog."""
    api = get_hf_api(token=token)
    try:
        endpoint = api.create_inference_endpoint_from_catalog(
            repo_id=repo,
            name=name,
            accelerator=accelerator,
            namespace=namespace,
            token=token,
        )
    except HfHubHTTPError as error:
        out.error(f"Deployment failed: {error}")
        raise typer.Exit(code=error.response.status_code) from error

    out.dict(endpoint.raw)

