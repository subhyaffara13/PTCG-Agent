from typing import Dict, Union

def _get_env(environment: Dict[str, str], name: str) -> str:
    value: Union[str, Undefined] = environment.get(name, _undefined)

    if isinstance(value, Undefined):
        raise UndefinedEnvironmentName(
            f"{name!r} does not exist in evaluation environment."
        )

    return value

