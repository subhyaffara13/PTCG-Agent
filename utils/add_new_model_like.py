
def add_new_model_like(
    repo_path: Annotated[
        str | None, typer.Argument(help="When not using an editable install, the path to the Transformers repo.")
    ] = None,
):
    """
    Add a new model to the library, based on an existing one.
    """
    (
        old_model_infos,
        new_lowercase_name,
        new_model_paper_name,
        filenames_to_add,
    ) = get_user_input()

    _add_new_model_like_internal(
        repo_path=Path(repo_path) if repo_path is not None else REPO_PATH,
        old_model_infos=old_model_infos,
        new_lowercase_name=new_lowercase_name,
        new_model_paper_name=new_model_paper_name,
        filenames_to_add=filenames_to_add,
    )

