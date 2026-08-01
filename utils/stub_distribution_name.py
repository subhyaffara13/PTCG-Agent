
def stub_distribution_name(module: str) -> str | None:
    top_level = module.split(".", 1)[0]

    dist = non_bundled_packages_flat.get(top_level)
    if dist:
        return dist

    if top_level in non_bundled_packages_namespace:
        namespace = non_bundled_packages_namespace[top_level]
        components = module.split(".")
        for i in range(len(components), 0, -1):
            module = ".".join(components[:i])
            dist = namespace.get(module)
            if dist:
                return dist

    return None

