from pathlib import Path


def _create_model_card(repo_dir: Path):
    """
    Creates a model card for the repository.

    Args:
        repo_dir (`Path`):
            Directory where model card is created.
    """
    readme_path = repo_dir / "README.md"

    if not readme_path.exists():
        with readme_path.open("w", encoding="utf-8") as f:
            f.write(README_TEMPLATE)

