
def resolve_aws_region_with_source(
    aws_region: str | None, *, session: object | None = None
) -> tuple[str, Literal["explicit", "environment", "profile"]]:
    region = aws_region
    source: Literal["explicit", "environment", "profile"] = "explicit"
    if region is None or not region.strip():
        region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        source = "environment"
    if (region is None or not region.strip()) and session is not None:
        get_config_variable = getattr(session, "get_config_variable", None)
        if callable(get_config_variable):
            region = cast("str | None", get_config_variable("region"))
            source = "profile"

    if region is None or not region.strip():
        raise OpenAIError(
            "Bedrock requires an AWS region. Pass `region` to `bedrock(...)`, or set `AWS_REGION` or "
            "`AWS_DEFAULT_REGION`."
        )

    return region.strip(), source

