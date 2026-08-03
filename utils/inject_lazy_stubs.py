import sys
from typing import Dict

def inject_lazy_stubs(schema: Dict) -> Dict:
    """Inject openapi entries for unloaded features. Uses the snapshot file
    when available (full route info), otherwise falls back to a single
    placeholder per feature. Any failure logs and returns the schema unchanged
    so /openapi.json never 500s on a cosmetic injection bug."""
    try:
        from litellm.proxy._lazy_openapi_snapshot import load_snapshot

        snapshot = load_snapshot()
        paths = schema.setdefault("paths", {})
        schemas = schema.setdefault("components", {}).setdefault("schemas", {})

        for feat in LAZY_FEATURES:
            if feat.module_path in sys.modules and not feat.persistent_swagger_stub:
                continue

            fragment = (snapshot or {}).get(feat.name)
            if fragment:
                for p, ops in fragment.get("paths", {}).items():
                    paths.setdefault(p, ops)
                for name, sch in (
                    fragment.get("components", {}).get("schemas", {}).items()
                ):
                    schemas.setdefault(name, sch)
                continue

            prefix = feat.path_prefixes[0]
            if prefix in paths:
                continue
            paths[prefix] = {
                "get": {
                    "tags": [feat.name],
                    "summary": feat.name,
                    "responses": {"200": {"description": "OK"}},
                }
            }
    except Exception as exc:
        verbose_proxy_logger.warning("inject_lazy_stubs failed: %s", exc)
    return schema

