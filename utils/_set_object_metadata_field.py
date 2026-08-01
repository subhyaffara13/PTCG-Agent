
def _set_object_metadata_field(
    object_data: Union[
        LiteLLM_TeamTable,
        KeyRequestBase,
        LiteLLM_OrganizationTable,
        LiteLLM_ProjectTable,
        "NewProjectRequest",
        "UpdateProjectRequest",
    ],
    field_name: str,
    value: Any,
) -> None:
    """
    Helper function to set metadata fields that require premium user checks

    Args:
        object_data: The team/key/organization/project data object to modify
        field_name: Name of the metadata field to set
        value: Value to set for the field
    """
    if field_name in LiteLLM_ManagementEndpoint_MetadataFields_Premium and value:
        _premium_user_check(field_name)

    object_data.metadata = object_data.metadata or {}
    object_data.metadata[field_name] = value

