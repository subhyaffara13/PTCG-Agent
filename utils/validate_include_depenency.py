
def validate_include_depenency(pyproject: T) -> T:
    dependency_groups = pyproject.get("dependency-groups", {})
    for key, value in dependency_groups.items():
        for each in value:
            if (
                isinstance(each, dict)
                and (include_group := each.get("include-group"))
                and include_group not in dependency_groups
            ):
                raise IncludedDependencyGroupMustExist(
                    message=f"The included dependency group {include_group} doesn't exist",
                    value=each,
                    name=f"data.dependency_groups.{key}",
                    definition={
                        "description": cleandoc(IncludedDependencyGroupMustExist._DESC),
                        "see": IncludedDependencyGroupMustExist._URL,
                    },
                    rule="PEP 735",
                )
    # TODO: check for `include-group` cycles (can be conditional to graphlib)
    return pyproject

