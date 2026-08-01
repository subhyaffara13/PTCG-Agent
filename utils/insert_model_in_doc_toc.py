
def insert_model_in_doc_toc(
    repo_path: Path, old_lowercase_name: str, new_lowercase_name: str, new_model_paper_name: str
):
    """
    Insert the new model in the doc `_toctree.yaml`, in the same section as the old model.

    Args:
        old_lowercase_name (`str`):
            The old lowercase model name.
        new_lowercase_name (`str`):
            The new lowercase model name.
        new_model_paper_name (`str`):
            The fully cased name (as in the official paper name) of the new model.
    """
    toc_file = repo_path / "docs" / "source" / "en" / "_toctree.yml"
    with open(toc_file, "r") as f:
        content = f.read()

    toc_match = re.search(rf"- local: model_doc/{old_lowercase_name}\n {{8}}title: .*?\n", content)
    if toc_match is None:
        raise ValueError(f"Could not find TOC entry for {old_lowercase_name}")
    old_model_toc = toc_match.group(0)
    new_toc = f"      - local: model_doc/{new_lowercase_name}\n        title: {new_model_paper_name}\n"
    add_content_to_file(
        repo_path / "docs" / "source" / "en" / "_toctree.yml", new_content=new_toc, add_after=old_model_toc
    )

