
def find_modular_structure(
    module_name: Path, old_model_infos: ModelInfos, new_cased_name: str
) -> tuple[str, str, list]:
    """
    Extract the modular structure that will be needed to copy a file `module_name` using modular.

    Args:
        module_name (`str`):
            The full path to the python module to copy with modular.
        old_model_infos (`ModelInfos`):
            The structure containing the class information of the old model.
        new_cased_name (`str`):
            The new cased model name.
    """
    all_classes, public_classes = find_all_classes_from_file(module_name)
    import_location = ".".join(module_name.parts[-2:]).replace(".py", "")
    old_cased_name = old_model_infos.camelcase_name
    imports = f"from ..{import_location} import {', '.join(class_ for class_ in all_classes)}"
    modular_classes = "\n\n".join(
        f"class {class_.replace(old_cased_name, new_cased_name)}({class_}):\n    pass" for class_ in all_classes
    )
    public_classes = [class_.replace(old_cased_name, new_cased_name) for class_ in public_classes]
    return imports, modular_classes, public_classes

