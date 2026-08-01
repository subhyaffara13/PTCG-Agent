
def _dep_warn(field):
    warnings.warn(
        dedent(
            f"""`{field}` kwargs of validate has been deprecated for security
        reasons, and will be removed soon.

        Please explicitly use the `n_changes, new_notebook = nbformat.validator.normalize(old_notebook, ...)` if you wish to
        normalise your notebook. `normalize` is available since nbformat 5.5.0

        """
        ),
        DeprecationWarning,
        stacklevel=3,
    )

