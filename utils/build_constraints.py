
def build_constraints() -> Option:
    return Option(
        "--build-constraint",
        dest="build_constraints",
        action="append",
        type="str",
        default=[],
        metavar="file",
        help=(
            "Constrain build dependencies using the given constraints file. "
            "This option can be used multiple times."
        ),
    )

