
def configuration_to_dict(
    handlers: Iterable[
        ConfigHandler[Distribution] | ConfigHandler[DistributionMetadata]
    ],
) -> dict:
    """Returns configuration data gathered by given handlers as a dict.

    :param Iterable[ConfigHandler] handlers: Handlers list,
        usually from parse_configuration()

    :rtype: dict
    """
    config_dict: dict = defaultdict(dict)

    for handler in handlers:
        for option in handler.set_options:
            value = _get_option(handler.target_obj, option)
            config_dict[handler.section_prefix][option] = value

    return config_dict

