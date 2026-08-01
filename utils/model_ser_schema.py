
def model_ser_schema(cls: type[Any], schema: CoreSchema) -> ModelSerSchema:
    """
    Returns a schema for serialization using a model.

    Args:
        cls: The expected class type, used to generate warnings if the wrong type is passed
        schema: Internal schema to use to serialize the model dict
    """
    return ModelSerSchema(type='model', cls=cls, schema=schema)

