
def _unify_entry_points(project_table: dict):
    project = project_table
    given = project.pop("entry-points", project.pop("entry_points", {}))
    entry_points = dict(given)  # Avoid problems with static
    renaming = {"scripts": "console_scripts", "gui_scripts": "gui_scripts"}
    for key, value in list(project.items()):  # eager to allow modifications
        norm_key = json_compatible_key(key)
        if norm_key in renaming:
            # Don't skip even if value is empty (reason: reset missing `dynamic`)
            entry_points[renaming[norm_key]] = project.pop(key)

    if entry_points:
        project["entry-points"] = {
            name: [f"{k} = {v}" for k, v in group.items()]
            for name, group in entry_points.items()
            if group  # now we can skip empty groups
        }

