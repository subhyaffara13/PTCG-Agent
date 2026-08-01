
def registry_add():
    resource = DRAFT202012.create_resource(schema)
    return registry.with_resource(uri="urn:example", resource=resource)

