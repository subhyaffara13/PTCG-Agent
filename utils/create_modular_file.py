
def create_modular_file(
    repo_path: Path,
    old_model_infos: ModelInfos,
    new_lowercase_name: str,
    filenames_to_add: list[tuple[str, bool]],
) -> str:
    """
    Create a new modular file which will copy the old model, based on the new name and the different filenames
    (modules) to add.

    Args:
        old_model_infos (`ModelInfos`):
            The structure containing the class information of the old model.
        new_lowercase_name (`str`):
            The new lowercase model name.
        filenames_to_add (`list[tuple[str, bool]]`):
            A list of tuples of all potential filenames to add for a new model, along a boolean flag describing if we
            should add this file or not. For example, [(`modeling_xxx.px`, True), (`configuration_xxx.py`, True), (`tokenization_xxx.py`, False),...]
    """
    new_cased_name = "".join(x.title() for x in new_lowercase_name.replace("-", "_").split("_"))
    old_lowercase_name = old_model_infos.lowercase_name
    old_folder_root = repo_path / "src" / "transformers" / "models" / old_lowercase_name

    # Construct the modular file from the original (old) model, by subclassing each class
    all_imports = ""
    all_bodies = ""
    all_public_classes = []
    for filename, to_add in filenames_to_add:
        if to_add:
            imports, body, public_classes = find_modular_structure(
                old_folder_root / filename, old_model_infos, new_cased_name
            )
            all_imports += f"\n{imports}"
            all_bodies += f"\n\n{body}"
            all_public_classes.extend(public_classes)

    # Create the __all__ assignment
    public_classes_formatted = "\n            ".join(f"{public_class}," for public_class in all_public_classes)
    all_statement = textwrap.dedent(
        f"""

        __all__ = [
            {public_classes_formatted}
        ]
        """
    )
    # Create the whole modular file
    modular_file = COPYRIGHT + all_imports + all_bodies + all_statement
    # Remove outer explicit quotes "" around the public class names before returning them
    all_public_classes = [public_class.replace('"', "") for public_class in all_public_classes]
    return modular_file, all_public_classes

