from typing import Any, Dict, Optional, Set, Tuple

def _apply_patch_ops(
    existing_user: LiteLLM_UserTable,
    patch_ops: SCIMPatchOp,
) -> Tuple[Dict[str, Any], Set[str]]:
    """Apply patch operations and return update data and final team set."""
    update_data: Dict[str, Any] = {}
    metadata = existing_user.metadata or {}
    scim_metadata = metadata.get("scim_metadata", {})

    teams_set: Set[str] = set(existing_user.teams or [])
    replace_team_set: Optional[Set[str]] = None

    for op in patch_ops.Operations:
        path = (op.path or "").lower()
        value = op.value
        op_type = op.op

        # Handle SCIM operations without path where value contains the fields
        if not path and isinstance(value, dict):
            for key, val in value.items():
                key_lower = key.lower()
                if key_lower == "active":
                    _handle_active_update(op_type, val, metadata)
                elif key_lower == "displayname":
                    _handle_displayname_update(op_type, val, update_data)
                elif key_lower == "externalid":
                    _handle_externalid_update(op_type, val, update_data)
                elif key_lower == "name" and isinstance(val, dict):
                    for name_key, name_val in val.items():
                        name_key_lower = name_key.lower()
                        if name_key_lower in ("givenname", "familyname"):
                            _handle_name_update(
                                f"name.{name_key_lower}",
                                op_type,
                                name_val,
                                scim_metadata,
                            )
            continue

        if path == "displayname":
            _handle_displayname_update(op_type, value, update_data)
        elif path == "externalid":
            _handle_externalid_update(op_type, value, update_data)
        elif path == "active":
            _handle_active_update(op_type, value, metadata)
        elif path in ("name.givenname", "name.familyname"):
            _handle_name_update(path, op_type, value, scim_metadata)
        elif path.startswith("groups"):
            new_replace_set = _handle_group_operations(op_type, value, teams_set)
            if new_replace_set is not None:
                replace_team_set = new_replace_set
        else:
            _handle_generic_metadata(path, op_type, value, metadata)

    final_team_set = replace_team_set if replace_team_set is not None else teams_set
    metadata["scim_metadata"] = scim_metadata
    update_data["metadata"] = metadata
    return update_data, final_team_set

