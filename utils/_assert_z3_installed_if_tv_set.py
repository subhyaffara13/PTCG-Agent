
def _assert_z3_installed_if_tv_set():
    if not (_HAS_Z3 or not config.translation_validation):
        raise AssertionError(
            "translation validation requires Z3 package. Please, either install "
            "z3-solver or disable translation validation."
        )

