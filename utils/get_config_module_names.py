
def get_config_module_names(filename: str | None, modules: list[str]) -> str:
    if not filename or not modules:
        return ""

    if not is_toml(filename):
        return ", ".join(f"[mypy-{module}]" for module in modules)

    return "module = ['%s']" % ("', '".join(sorted(modules)))

