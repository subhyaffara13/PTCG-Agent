from typing import Optional

def _get_public_model_name(
    patch_data: updateDeployment,
    db_model: Deployment,
) -> str:
    """Determine the public model name from patch or existing model.

    The top-level ``model_name`` is the rename channel. For team-scoped rows
    the DB ``model_name`` column holds an internal routing key
    (``model_name_{team_id}_{uuid}``), and ``/model/info`` historically leaked
    it into the dashboard edit form, so a non-rename save (e.g. a TPM tweak)
    would PATCH the internal name and the update path would treat it as a
    rename -- overwriting ``team_public_model_name`` and rewriting the team ACL
    (see issue #28382).

    Guard against that by ignoring an incoming ``model_name`` that matches the
    internal shape, or is a no-op against the current DB column. Anything else
    is a genuine rename and wins. We deliberately do NOT read
    ``patch_data.model_info.team_public_model_name``: the dashboard passes the
    existing ``model_info`` blob through untouched on a rename, so honoring it
    would return the OLD public name and silently drop the rename.

    Precedence (highest first):
    1. patch_data.model_name -- a genuine rename: not internal-shape and not a
       no-op against db_model.model_name.
    2. db_model.model_info.team_public_model_name -- existing public name.
    3. db_model.model_name -- last-resort fallback for legacy rows.
    """
    team_id = (patch_data.model_info.team_id if patch_data.model_info else None) or (
        db_model.model_info.team_id if db_model.model_info else None
    )

    def _is_internal_shape(name: Optional[str]) -> bool:
        if team_id is None or not name:
            return False
        return name.startswith(f"model_name_{team_id}_")

    incoming = patch_data.model_name
    if (
        incoming
        and not _is_internal_shape(incoming)
        and incoming != db_model.model_name
    ):
        return incoming

    if db_model.model_info and db_model.model_info.team_public_model_name:
        return db_model.model_info.team_public_model_name

    return db_model.model_name

