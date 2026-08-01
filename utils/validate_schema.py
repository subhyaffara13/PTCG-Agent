
def validate_schema(schema: FunctionSchema) -> None:
    if not torch._library.utils.is_functional_schema(schema):
        raise ValueError(
            f"custom_op only supports functional operators "
            f"(ops that do not mutate any inputs, do not return "
            f"views of the inputs, and has at least one return). "
            f"Got the following non-functional schema: {schema}"
        )

    # For simplicity: don't allow self arguments
    if schema.arguments.self_arg is not None:
        raise ValueError(
            f"custom_op does not support arguments named 'self'. Please "
            f"rename your argument. Got: {schema}"
        )


def validate_schema(schema: dict, response: str):
    """
    Validate if the returned json response follows the schema.

    Params:
    - schema - dict: JSON schema
    - response - str: Received json response as string.
    """
    from jsonschema import ValidationError, validate

    from litellm import JSONSchemaValidationError

    try:
        response_dict = json.loads(response)
    except json.JSONDecodeError:
        raise JSONSchemaValidationError(
            model="", llm_provider="", raw_response=response, schema=json.dumps(schema)
        )

    try:
        validate(response_dict, schema=schema)
    except ValidationError:
        raise JSONSchemaValidationError(
            model="", llm_provider="", raw_response=response, schema=json.dumps(schema)
        )

