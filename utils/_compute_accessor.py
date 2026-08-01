
def _compute_accessor(parent_fqn: str, child_fqn: str) -> str:
    if parent_fqn == "":
        # Handle the root module correctly.
        return child_fqn

    parent_split = parent_fqn.split(".")
    child_split = child_fqn.split(".")

    # TODO: support skip connection by inlining the child module.
    if child_split[: len(parent_split)] != parent_split:
        raise RuntimeError(
            f"Child module '{child_fqn}' is not a descendant of parent module '{parent_fqn}'."
            "This is currently unsupported."
            "Please try to make child module attach to parent module directly."
        )
    return ".".join(child_split[len(parent_split) :])

