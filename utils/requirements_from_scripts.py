
def requirements_from_scripts() -> Option:
    return Option(
        "--requirements-from-script",
        action="append",
        default=[],
        dest="requirements_from_scripts",
        metavar="file",
        help="Install dependencies of the given script file "
        "as defined by PEP 723 inline metadata. ",
    )

