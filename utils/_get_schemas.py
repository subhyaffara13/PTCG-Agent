
def _get_schemas() -> list:
    """Return the list of SCIM Schema definitions per RFC 7643 Section 7."""
    return [
        SCIMSchema(
            id="urn:ietf:params:scim:schemas:core:2.0:User",
            name="User",
            description="User Account",
            attributes=[
                SCIMSchemaAttribute(
                    name="userName",
                    type="string",
                    multiValued=False,
                    description="Unique identifier for the User.",
                    required=True,
                    mutability="readWrite",
                    returned="default",
                    uniqueness="server",
                ),
                SCIMSchemaAttribute(
                    name="name",
                    type="complex",
                    multiValued=False,
                    description="The components of the user's real name.",
                    required=False,
                    subAttributes=[
                        SCIMSchemaAttribute(
                            name="givenName",
                            type="string",
                            description="The given name of the User.",
                        ),
                        SCIMSchemaAttribute(
                            name="familyName",
                            type="string",
                            description="The family name of the User.",
                        ),
                        SCIMSchemaAttribute(
                            name="formatted",
                            type="string",
                            description="The full name.",
                        ),
                    ],
                ),
                SCIMSchemaAttribute(
                    name="displayName",
                    type="string",
                    multiValued=False,
                    description="The name of the User, suitable for display.",
                ),
                SCIMSchemaAttribute(
                    name="emails",
                    type="complex",
                    multiValued=True,
                    description="Email addresses for the user.",
                    subAttributes=[
                        SCIMSchemaAttribute(
                            name="value",
                            type="string",
                            description="Email address value.",
                        ),
                        SCIMSchemaAttribute(
                            name="type",
                            type="string",
                            description="Type of email (work, home, etc.).",
                        ),
                        SCIMSchemaAttribute(
                            name="primary",
                            type="boolean",
                            description="Whether this is the primary email.",
                        ),
                    ],
                ),
                SCIMSchemaAttribute(
                    name="active",
                    type="boolean",
                    multiValued=False,
                    description="Whether the user account is active.",
                ),
                SCIMSchemaAttribute(
                    name="groups",
                    type="complex",
                    multiValued=True,
                    description="Groups to which the user belongs.",
                    mutability="readOnly",
                    subAttributes=[
                        SCIMSchemaAttribute(
                            name="value",
                            type="string",
                            description="Group identifier.",
                        ),
                        SCIMSchemaAttribute(
                            name="display",
                            type="string",
                            description="Group display name.",
                        ),
                    ],
                ),
            ],
            meta={
                "location": "/scim/v2/Schemas/urn:ietf:params:scim:schemas:core:2.0:User",
                "resourceType": "Schema",
            },
        ),
        SCIMSchema(
            id="urn:ietf:params:scim:schemas:core:2.0:Group",
            name="Group",
            description="Group",
            attributes=[
                SCIMSchemaAttribute(
                    name="displayName",
                    type="string",
                    multiValued=False,
                    description="A human-readable name for the Group.",
                    required=True,
                    mutability="readWrite",
                    returned="default",
                    uniqueness="none",
                ),
                SCIMSchemaAttribute(
                    name="members",
                    type="complex",
                    multiValued=True,
                    description="A list of members of the Group.",
                    subAttributes=[
                        SCIMSchemaAttribute(
                            name="value",
                            type="string",
                            description="Member identifier.",
                        ),
                        SCIMSchemaAttribute(
                            name="display",
                            type="string",
                            description="Member display name.",
                        ),
                    ],
                ),
            ],
            meta={
                "location": "/scim/v2/Schemas/urn:ietf:params:scim:schemas:core:2.0:Group",
                "resourceType": "Schema",
            },
        ),
    ]

