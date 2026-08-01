
def add_provider_specific_fields(
    object: BaseModel, provider_specific_fields: Optional[Dict[str, Any]]
):
    if not provider_specific_fields:  # set if provider_specific_fields is not empty
        return
    setattr(object, "provider_specific_fields", provider_specific_fields)

