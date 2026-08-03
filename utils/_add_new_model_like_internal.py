import os
import subprocess
from pathlib import Path


def _add_new_model_like_internal(
    repo_path: Path,
    old_model_infos: ModelInfos,
    new_lowercase_name: str,
    new_model_paper_name: str,
    filenames_to_add: list[tuple[str, bool]],
):
    """
    Creates a new model module like a given model of the Transformers library.

    Args:
        repo_path (`Path`):
            The path to the root of the Transformers repository.
        old_model_infos (`ModelInfos`):
            The structure containing the class information of the old model.
        new_lowercase_name (`str`):
            The new lowercase model name.
        new_model_paper_name (`str`):
            The fully cased name (as in the official paper name) of the new model.
        filenames_to_add (`list[tuple[str, bool]]`):
            A list of tuples of all potential filenames to add for a new model, along a boolean flag describing if we
            should add this file or not. For example, [(`modeling_xxx.px`, True), (`configuration_xxx.py`, True), (`tokenization_xxx.py`, False),...]
    """
    # As the import was protected, raise if not present (as it's actually a hard dependency for this command)
    if not is_libcst_available():
        raise ValueError("You need to install `libcst` to run this command -> `pip install libcst`")

    old_lowercase_name = old_model_infos.lowercase_name

    # 1. We create the folder for our new model
    new_module_folder = repo_path / "src" / "transformers" / "models" / new_lowercase_name
    os.makedirs(new_module_folder, exist_ok=True)

    # 2. Create and add the modular file
    modular_file, public_classes = create_modular_file(
        repo_path, old_model_infos, new_lowercase_name, filenames_to_add
    )
    with open(new_module_folder / f"modular_{new_lowercase_name}.py", "w") as f:
        f.write(modular_file)

    # 3. Create and add the __init__.py
    init_file = create_init_file(old_lowercase_name, new_lowercase_name, filenames_to_add)
    with open(new_module_folder / "__init__.py", "w") as f:
        f.write(init_file)

    # 4. Add new model to the models init
    add_content_to_file(
        repo_path / "src" / "transformers" / "models" / "__init__.py",
        new_content=f"    from .{new_lowercase_name} import *\n",
        add_after="if TYPE_CHECKING:\n",
    )

    # 5. Add model to auto mappings
    add_model_to_auto_mappings(repo_path, old_model_infos, new_lowercase_name, new_model_paper_name, filenames_to_add)

    # 6. Add test files
    tests_folder = repo_path / "tests" / "models" / new_lowercase_name
    os.makedirs(tests_folder, exist_ok=True)
    # Add empty __init__.py
    with open(tests_folder / "__init__.py", "w"):
        pass
    test_files = create_test_files(repo_path, old_model_infos, new_lowercase_name, filenames_to_add)
    for filename, content in test_files.items():
        with open(tests_folder / filename, "w") as f:
            f.write(content)

    # 7. Add doc file
    doc_file = create_doc_file(new_model_paper_name, public_classes)
    with open(repo_path / "docs" / "source" / "en" / "model_doc" / f"{new_lowercase_name}.md", "w") as f:
        f.write(doc_file)
    insert_model_in_doc_toc(repo_path, old_lowercase_name, new_lowercase_name, new_model_paper_name)

    # 9. Run linters
    model_init_file = repo_path / "src" / "transformers" / "models" / "__init__.py"
    subprocess.run(
        ["ruff", "check", new_module_folder, tests_folder, model_init_file, "--fix"],
        cwd=repo_path,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["ruff", "format", new_module_folder, tests_folder, model_init_file],
        cwd=repo_path,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["python", "utils/check_doc_toc.py", "--fix_and_overwrite"], cwd=repo_path, stdout=subprocess.DEVNULL
    )
    subprocess.run(["python", "utils/sort_auto_mappings.py"], cwd=repo_path, stdout=subprocess.DEVNULL)

    # 10. Run the modular conversion
    subprocess.run(
        ["python", "utils/modular_model_converter.py", new_lowercase_name], cwd=repo_path, stdout=subprocess.DEVNULL
    )

