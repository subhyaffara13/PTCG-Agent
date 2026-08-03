import copy
from typing import Any

def _redact_callback_secrets(metadata: Any) -> Any:
    """Strip secret values out of a team-metadata snapshot before audit logging.

    Both ``team_metadata["logging"]`` (list of ``AddTeamCallback`` dicts) and
    ``team_metadata["callback_settings"]["callback_vars"]`` carry provider
    credentials such as ``langfuse_secret_key``, ``langsmith_api_key``, and
    ``gcs_path_service_account``.  Persisting them verbatim into
    ``LiteLLM_AuditLogs`` would let anyone with read access to the audit
    table harvest team callback credentials, so we replace each value with
    a fixed marker.  The keys themselves are kept so the audit reader can
    still see *which* fields changed.
    """
    if not isinstance(metadata, dict):
        return metadata
    redacted = copy.deepcopy(metadata)
    logging_entries = redacted.get("logging")
    if isinstance(logging_entries, list):
        for entry in logging_entries:
            if isinstance(entry, dict) and isinstance(entry.get("callback_vars"), dict):
                entry["callback_vars"] = {
                    k: _CALLBACK_VARS_REDACTED for k in entry["callback_vars"]
                }
    callback_settings = redacted.get("callback_settings")
    if isinstance(callback_settings, dict) and isinstance(
        callback_settings.get("callback_vars"), dict
    ):
        callback_settings["callback_vars"] = {
            k: _CALLBACK_VARS_REDACTED for k in callback_settings["callback_vars"]
        }
    return redacted

