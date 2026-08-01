
def _scrub_db_overlay_remote_module_loads(section: str, db_value: Any) -> Any:
    """Strip ``s3://`` / ``gcs://`` entries from the DB-overlay value for
    fields whose contents reach ``get_instance_fn``. The same scheme is
    allowed from a YAML config (the documented operator flow) but a
    DB-overlay write would otherwise smuggle the same payload through
    the YAML-load chain and reach ``_load_instance_from_remote_storage``."""
    if not isinstance(db_value, dict):
        return db_value
    str_fields = _DB_OVERLAY_REMOTE_MODULE_STR_FIELDS.get(section, ())
    list_fields = _DB_OVERLAY_REMOTE_MODULE_LIST_FIELDS.get(section, ())
    if not str_fields and not list_fields and section != "general_settings":
        return db_value
    sanitized = copy.deepcopy(db_value)
    for field in str_fields:
        v = sanitized.get(field)
        if _is_remote_module_url(v):
            verbose_proxy_logger.warning(
                "Refused remote-URL value for DB-overlay %s.%s=%r; only "
                "config.yaml entries may reference s3:// / gcs:// modules.",
                section,
                field,
                v,
            )
            sanitized[field] = None
    for field in list_fields:
        v = sanitized.get(field)
        if isinstance(v, list):
            cleaned = [item for item in v if not _is_remote_module_url(item)]
            if len(cleaned) != len(v):
                verbose_proxy_logger.warning(
                    "Refused %d remote-URL entries from DB-overlay %s.%s; "
                    "only config.yaml entries may reference s3:// / gcs:// "
                    "modules.",
                    len(v) - len(cleaned),
                    section,
                    field,
                )
                sanitized[field] = cleaned
    # ``custom_provider_map`` is a list of dicts with ``custom_handler`` —
    # walk it explicitly.
    if section == "litellm_settings":
        cpm = sanitized.get("custom_provider_map")
        if isinstance(cpm, list):
            for item in cpm:
                if isinstance(item, dict) and _is_remote_module_url(
                    item.get("custom_handler")
                ):
                    verbose_proxy_logger.warning(
                        "Refused remote-URL custom_handler from DB-overlay "
                        "litellm_settings.custom_provider_map: %r",
                        item.get("custom_handler"),
                    )
                    item["custom_handler"] = None
    # ``litellm_settings.guardrails`` is a list of single-key dicts in
    # v1 ({guardrail_name: {callbacks: [...], default_on: bool}}) or a
    # list of v2 entries ({guardrail_name, litellm_params: {guardrail:
    # "module.path", callbacks: [...]}}). Both shapes terminate in
    # ``callbacks`` (a list) or ``guardrail`` (a single dotted name)
    # that flow into ``get_instance_fn`` during config load.
    if section == "litellm_settings":
        guardrails = sanitized.get("guardrails")
        if isinstance(guardrails, list):
            for entry in guardrails:
                if not isinstance(entry, dict):
                    continue
                for inner in entry.values():
                    if not isinstance(inner, dict):
                        continue
                    _scrub_guardrail_inner(inner)
                lp = entry.get("litellm_params")
                if isinstance(lp, dict):
                    _scrub_guardrail_inner(lp)

    # ``general_settings.litellm_jwtauth.custom_validate`` is a nested
    # string field.
    if section == "general_settings":
        jwt = sanitized.get("litellm_jwtauth")
        if isinstance(jwt, dict) and _is_remote_module_url(jwt.get("custom_validate")):
            verbose_proxy_logger.warning(
                "Refused remote-URL custom_validate from DB-overlay "
                "general_settings.litellm_jwtauth: %r",
                jwt.get("custom_validate"),
            )
            jwt["custom_validate"] = None
        # ``pass_through_endpoints`` is a list of dicts whose ``target``
        # is passed through ``create_pass_through_route`` →
        # ``get_instance_fn``. A DB-overlay ``target: "s3://attacker/m.i"``
        # would otherwise reach the loader because the YAML-load chain
        # has ``config_file_path`` set.
        pte = sanitized.get("pass_through_endpoints")
        if isinstance(pte, list):
            for entry in pte:
                if isinstance(entry, dict) and _is_remote_module_url(
                    entry.get("target")
                ):
                    verbose_proxy_logger.warning(
                        "Refused remote-URL target from DB-overlay "
                        "general_settings.pass_through_endpoints "
                        "(path=%r): %r",
                        entry.get("path"),
                        entry.get("target"),
                    )
                    entry["target"] = None
    return sanitized

