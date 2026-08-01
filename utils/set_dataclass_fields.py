
def set_dataclass_fields(
    cls: type[StandardDataclass],
    config_wrapper: _config.ConfigWrapper,
    ns_resolver: NsResolver | None = None,
) -> None:
    """Collect and set `cls.__pydantic_fields__`.

    Args:
        cls: The class.
        config_wrapper: The config wrapper instance.
        ns_resolver: Namespace resolver to use when getting dataclass annotations.
    """
    typevars_map = get_standard_typevars_map(cls)
    fields = collect_dataclass_fields(
        cls, ns_resolver=ns_resolver, typevars_map=typevars_map, config_wrapper=config_wrapper
    )

    cls.__pydantic_fields__ = fields  # type: ignore

