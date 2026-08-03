from typing import Any, Dict, Tuple

def add_access_group_to_deployment(
    model_info: Dict[str, Any], access_group: str
) -> Tuple[Dict[str, Any], bool]:
    """
    Add an access group to a deployment's model_info.

    Args:
        model_info: The model_info dictionary from the deployment
        access_group: The access group name to add

    Returns:
        Tuple[Dict[str, Any], bool]: (updated_model_info, was_modified)
    """
    access_groups = model_info.get("access_groups", [])

    # Check if access group already exists
    if access_group in access_groups:
        return model_info, False

    # Add the access group
    access_groups.append(access_group)
    model_info["access_groups"] = access_groups

    return model_info, True

