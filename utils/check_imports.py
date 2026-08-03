import os

def check_imports(filename: str | os.PathLike) -> list[str]:
    """
    Check if the current Python environment contains all the libraries that are imported in a file. Will raise if a
    library is missing.

    Args:
        filename (`str` or `os.PathLike`): The module file to check.

    Returns:
        `list[str]`: The list of relative imports in the file.
    """
    imports = get_imports(filename)
    missing_packages = []
    for imp in imports:
        try:
            importlib.import_module(imp)
        except ImportError as exception:
            logger.warning(f"Encountered exception while importing {imp}: {exception}")
            # Some packages can fail with an ImportError because of a dependency issue.
            # This check avoids hiding such errors.
            # See https://github.com/huggingface/transformers/issues/33604
            if "No module named" in str(exception):
                missing_packages.append(imp)
            else:
                raise

    if len(missing_packages) > 0:
        raise ImportError(
            "This modeling file requires the following packages that were not found in your environment: "
            f"{', '.join(missing_packages)}. Run `pip install {' '.join(missing_packages)}`"
        )

    return get_relative_imports(filename)

