
def detailed_errors() -> Generator[None, None, None]:
    try:
        yield
    except JsonSchemaValueException as ex:
        raise ValidationError._from_jsonschema(ex) from None

