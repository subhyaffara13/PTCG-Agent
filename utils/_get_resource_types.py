
def _get_resource_types(base_url: str = "/scim/v2") -> list:
    """Return the list of SCIM ResourceType definitions per RFC 7643 Section 6."""
    return [
        SCIMResourceType(
            id="User",
            name="User",
            description="User Account",
            endpoint="/Users",
            schema_="urn:ietf:params:scim:schemas:core:2.0:User",
            meta={
                "location": f"{base_url}/ResourceTypes/User",
                "resourceType": "ResourceType",
            },
        ),
        SCIMResourceType(
            id="Group",
            name="Group",
            description="Group",
            endpoint="/Groups",
            schema_="urn:ietf:params:scim:schemas:core:2.0:Group",
            meta={
                "location": f"{base_url}/ResourceTypes/Group",
                "resourceType": "ResourceType",
            },
        ),
    ]

