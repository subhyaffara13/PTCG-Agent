
def make_dataclass_validator(dc_cls: Type['Dataclass'], config: Type[BaseConfig]) -> 'CallableGenerator':
    """
    Create a pydantic.dataclass from a builtin dataclass to add type validation
    and yield the validators
    It retrieves the parameters of the dataclass and forwards them to the newly created dataclass
    """
    yield from _get_validators(dataclass(dc_cls, config=config, use_proxy=True))

