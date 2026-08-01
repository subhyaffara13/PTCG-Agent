
def dataclass_fields(cls: Any) -> Any:
    return torch._dynamo.disable(dataclasses.fields)(cls)

