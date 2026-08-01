
def _check_dill_version(pickle_module) -> None:
    """Checks if using dill as the pickle module, and if so, checks if it is the correct version.
    If dill version is lower than 0.3.1, a ValueError is raised.

    Args:
        pickle_module: module used for pickling metadata and objects

    """
    if pickle_module is not None and pickle_module.__name__ == "dill":
        required_dill_version = (0, 3, 1)
        if not check_module_version_greater_or_equal(
            pickle_module, required_dill_version, False
        ):
            raise ValueError(
                (
                    "'torch' supports dill >= {}, but you have dill {}."
                    " Please upgrade dill or switch to 'pickle'"
                ).format(
                    ".".join([str(num) for num in required_dill_version]),
                    pickle_module.__version__,
                )
            )

