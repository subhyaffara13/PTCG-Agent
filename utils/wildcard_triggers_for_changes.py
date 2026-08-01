
def wildcard_triggers_for_changes(module_id: str, diff: set[str]) -> set[str]:
    """Return catch-all wildcard triggers activated by a set of changed names."""
    result: set[str] = set()
    package_nesting_level = module_id.count(".")
    for item in diff:
        if item.count(".") <= package_nesting_level + 1 and item.split(".")[-1] not in (
            "__builtins__",
            "__file__",
            "__name__",
            "__package__",
            "__doc__",
        ):
            # Activate catch-all wildcard trigger for top-level module changes (used for
            # "from m import *"). This also gets triggered by changes to module-private
            # entries, but as these unneeded dependencies only result in extra processing,
            # it's a minor problem.
            #
            # TODO: Some __* names cause mistriggers. Fix the underlying issue instead of
            #     special casing them here.
            result.add(module_id + WILDCARD_TAG)
        if item.count(".") > package_nesting_level + 1:
            # These are for changes within classes, used by protocols.
            result.add(item.rsplit(".", 1)[0] + WILDCARD_TAG)
    return result

