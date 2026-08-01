
def get_module_from_module_name(module_name: str) -> ModuleType | None:
    # Module name can be uppercase in vendor.txt for some reason...
    module_name = module_name.lower().replace("-", "_")
    # PATCH: setuptools is actually only pkg_resources.
    if module_name == "setuptools":
        module_name = "pkg_resources"

    __import__(f"pip._vendor.{module_name}", globals(), locals(), level=0)
    return getattr(pip._vendor, module_name)

