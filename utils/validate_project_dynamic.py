
def validate_project_dynamic(pyproject: T) -> T:
    project_table = pyproject.get("project", {})
    dynamic = project_table.get("dynamic", [])

    for field in dynamic:
        if field in project_table:
            raise RedefiningStaticFieldAsDynamic(
                message=f"You cannot provide a value for `project.{field}` and "
                "list it under `project.dynamic` at the same time",
                value={
                    field: project_table[field],
                    "...": " # ...",
                    "dynamic": dynamic,
                },
                name=f"data.project.{field}",
                definition={
                    "description": cleandoc(RedefiningStaticFieldAsDynamic._DESC),
                    "see": RedefiningStaticFieldAsDynamic._URL,
                },
                rule="PEP 621",
            )

    return pyproject

