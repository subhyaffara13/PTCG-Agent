
def use_feature() -> Option:
    return Option(
    "--use-feature",
    dest="use_features",
    action="append",
    default=[],
    help="Enable new functionality, that may be backward incompatible.",
)

