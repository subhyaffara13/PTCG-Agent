
def get_test_extension_registry() -> ExtensionRegistry:
    registry = ExtensionRegistry()
    registry.register(Rot13Example)
    return registry

