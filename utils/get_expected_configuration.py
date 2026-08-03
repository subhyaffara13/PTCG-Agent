import copy
import json

def get_expected_configuration(
    configuration_path: str, default_configuration: PylintConfiguration
) -> PylintConfiguration:
    """Get the expected parsed configuration of a configuration functional test."""
    result = copy.deepcopy(default_configuration)
    config_as_json = get_expected_or_default(
        configuration_path, suffix="result.json", default="{}"
    )
    to_override = json.loads(config_as_json)
    for key, value in to_override.items():
        if key == EXPECTED_CONF_APPEND_KEY:
            for fkey, fvalue in value.items():
                result[fkey] += fvalue
        elif key == EXPECTED_CONF_REMOVE_KEY:
            for fkey, fvalue in value.items():
                new_value = []
                for old_value in result[fkey]:
                    if old_value not in fvalue:
                        new_value.append(old_value)
                result[fkey] = new_value
        else:
            result[key] = value
    return result

