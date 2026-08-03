from typing import Any

def resolve_properties(
    mark: Mark, data: DataFrame, scales: dict[str, Scale]
) -> dict[str, Any]:

    props = {
        name: mark._resolve(data, name, scales) for name in mark._mappable_props
    }
    return props

