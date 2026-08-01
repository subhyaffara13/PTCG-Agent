
def remove_access_group_from_deployment(
    model_info: Dict[str, Any], access_group: str
) -> Tuple[Dict[str, Any], bool]:
    """
    Remove an access group from a deployment's model_info.

    Args:
        model_info: The model_info dictionary from the deployment
        access_group: The access group name to remove

    Returns:
        Tuple[Dict[str, Any], bool]: (updated_model_info, was_modified)
    """
    access_groups = model_info.get("access_groups", [])

    # Check if access group exists
    if access_group not in access_groups:
        return model_info, False

    # Remove the access group
    access_groups.remove(access_group)
    model_info["access_groups"] = access_groups

    return model_info, True

