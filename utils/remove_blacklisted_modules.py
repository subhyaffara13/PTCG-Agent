
def remove_blacklisted_modules(modules: list[StubSource]) -> list[StubSource]:
    return [
        module for module in modules if module.path is None or not is_blacklisted_path(module.path)
    ]

