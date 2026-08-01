
def deploy(
    name: NameArg,
    repo: Annotated[
        str,
        typer.Option(
            help="The name of the model repository associated with the Inference Endpoint (e.g. 'openai/gpt-oss-120b').",
        ),
    ],
    framework: Annotated[
        str,
        typer.Option(
            help="The machine learning framework used for the model (e.g. 'vllm').",
        ),
    ],
    accelerator: Annotated[
        str,
        typer.Option(
            help="The hardware accelerator to be used for inference (e.g. 'cpu').",
        ),
    ],
    instance_size: Annotated[
        str,
        typer.Option(
            help="The size or type of the instance to be used for hosting the model (e.g. 'x4').",
        ),
    ],
    instance_type: Annotated[
        str,
        typer.Option(
            help="The cloud instance type where the Inference Endpoint will be deployed (e.g. 'intel-icl').",
        ),
    ],
    region: Annotated[
        str,
        typer.Option(
            help="The cloud region in which the Inference Endpoint will be created (e.g. 'us-east-1').",
        ),
    ],
    vendor: Annotated[
        str,
        typer.Option(
            help="The cloud provider or vendor where the Inference Endpoint will be hosted (e.g. 'aws').",
        ),
    ],
    *,
    namespace: NamespaceOpt = None,
    task: Annotated[
        str | None,
        typer.Option(
            help="The task on which to deploy the model (e.g. 'text-classification').",
        ),
    ] = None,
    token: TokenOpt = None,
    min_replica: Annotated[
        int,
        typer.Option(
            help="The minimum number of replicas (instances) to keep running for the Inference Endpoint.",
        ),
    ] = 1,
    max_replica: Annotated[
        int,
        typer.Option(
            help="The maximum number of replicas (instances) to scale to for the Inference Endpoint.",
        ),
    ] = 1,
    scale_to_zero_timeout: Annotated[
        int | None,
        typer.Option(
            help="The duration in minutes before an inactive endpoint is scaled to zero.",
        ),
    ] = None,
    scaling_metric: Annotated[
        InferenceEndpointScalingMetric | None,
        typer.Option(
            help="The metric reference for scaling.",
        ),
    ] = None,
    scaling_threshold: Annotated[
        float | None,
        typer.Option(
            help="The scaling metric threshold used to trigger a scale up. Ignored when scaling metric is not provided.",
        ),
    ] = None,
    revision: RevisionOpt = None,
    custom_image: Annotated[
        str | None,
        typer.Option(
            "--custom-image",
            help="Docker image URL for a custom container (e.g. 'nexagi/sglang:v0.5.12'). Requires '--framework custom'.",
        ),
    ] = None,
    health_route: Annotated[
        str | None,
        typer.Option(
            help="Health check route exposed by the custom container (e.g. '/health'). Requires --custom-image.",
        ),
    ] = None,
    port: Annotated[
        int | None,
        typer.Option(
            help="Port the custom container listens on (e.g. 30000). Requires --custom-image.",
        ),
    ] = None,
    container_command: Annotated[
        str | None,
        typer.Option(
            "--container-command",
            help=(
                "Override the container entrypoint, as a quoted string split into tokens "
                '(e.g. "python -m sglang.launch_server"). Requires --custom-image.'
            ),
        ),
    ] = None,
    container_args: Annotated[
        str | None,
        typer.Option(
            "--container-args",
            help=(
                "Arguments appended to the container entrypoint, as a quoted string split into tokens "
                '(e.g. "--tp 8 --reasoning-parser qwen3"). Requires --custom-image.'
            ),
        ),
    ] = None,
    env: EnvOpt = None,
    env_file: EnvFileOpt = None,
    secrets: SecretsOpt = None,
    secrets_file: SecretsFileOpt = None,
    endpoint_type: Annotated[
        str | None,
        typer.Option(
            "--type",
            click_type=SoftChoice(InferenceEndpointType),
            help="Endpoint access type. Defaults to 'authenticated' (token-gated, publicly reachable).",
        ),
    ] = None,
) -> None:
    """Deploy an Inference Endpoint from a Hub repository."""
    # Custom-container knobs only make sense alongside a custom image.
    if custom_image is None and (health_route is not None or port is not None or container_command or container_args):
        raise CLIError("--health-route, --port, --container-command and --container-args require --custom-image.")
    custom_image_dict: dict | None = None
    if custom_image is not None:
        custom_image_dict = {"url": custom_image}
        if health_route is not None:
            custom_image_dict["healthRoute"] = health_route
        if port is not None:
            custom_image_dict["port"] = port

    env_map = {key: value or "" for key, value in parse_env_map(env, env_file).items()}
    secrets_map = {key: value or "" for key, value in parse_env_map(secrets, secrets_file).items()}

    # Only forward the values the user actually set and let `create_inference_endpoint` own the defaults.
    params: dict = {}
    if endpoint_type is not None:
        params["type"] = endpoint_type
    if custom_image_dict is not None:
        params["custom_image"] = custom_image_dict
    if container_command:
        params["container_command"] = shlex.split(container_command)
    if container_args:
        params["container_args"] = shlex.split(container_args)
    if env_map:
        params["env"] = env_map
    if secrets_map:
        params["secrets"] = secrets_map

    api = get_hf_api(token=token)
    endpoint = api.create_inference_endpoint(
        name=name,
        repository=repo,
        framework=framework,
        accelerator=accelerator,
        instance_size=instance_size,
        instance_type=instance_type,
        region=region,
        vendor=vendor,
        namespace=namespace,
        task=task,
        token=token,
        min_replica=min_replica,
        max_replica=max_replica,
        scaling_metric=scaling_metric,
        scaling_threshold=scaling_threshold,
        scale_to_zero_timeout=scale_to_zero_timeout,
        revision=revision,
        **params,
    )
    out.dict(endpoint.raw)
    out.hint(f"Use 'hf endpoints describe {name}' to check the deployment status.")

