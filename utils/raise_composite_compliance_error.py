
def raise_composite_compliance_error(err, additional_info=''):
    raise RuntimeError(
        "Composite compliance check failed with "
        "the above error.\n"
        f"{additional_info}"
        "If you are adding an OpInfo of an "
        "existing operator, please feel free to skip this test "
        "because the problem was pre-existing and file an issue. "
        "Otherwise, if you added a new operator, please read "
        "through the Composite Compliance section in "
        "aten/src/ATen/native/README.md for how to resolve this. "
    ) from err

