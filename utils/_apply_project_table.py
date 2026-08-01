
def _apply_project_table(dist: Distribution, config: dict, root_dir: StrPath):
    orig_config = config.get("project", {})
    if not orig_config:
        return  # short-circuit

    project_table = {k: _static.attempt_conversion(v) for k, v in orig_config.items()}
    _handle_missing_dynamic(dist, project_table)
    _unify_entry_points(project_table)

    for field, value in project_table.items():
        norm_key = json_compatible_key(field)
        corresp = PYPROJECT_CORRESPONDENCE.get(norm_key, norm_key)
        if callable(corresp):
            corresp(dist, value, root_dir)
        else:
            _set_config(dist, corresp, value)

