
def _make_warmup_router(app: "FastAPI") -> "APIRouter":
    """POST /lazy/warm/{name}: load a feature and return its partial openapi
    so the Swagger plugin can merge in-place without a full /openapi.json refetch.
    Requires auth — anyone who can hit the proxy can already trigger the same
    imports by sending a real request to a feature's prefix, but gating this
    debug endpoint avoids unauthenticated callers forcing the import chain."""
    from fastapi import APIRouter, Depends, HTTPException
    from fastapi.openapi.utils import get_openapi

    from litellm.proxy.auth.user_api_key_auth import user_api_key_auth

    router = APIRouter()

    @router.post(
        "/lazy/warm/{name}",
        include_in_schema=False,
        dependencies=[Depends(user_api_key_auth)],
    )
    async def warm(name: str):
        feat = next((f for f in LAZY_FEATURES if f.name == name), None)
        if feat is None:
            raise HTTPException(404, f"unknown lazy feature: {name}")
        if feat.persistent_swagger_stub:
            return {"stub_path": None, "paths": {}, "components": {"schemas": {}}}

        await _force_load(app, feat)

        feat_routes = [r for r in app.routes if feat.matches(getattr(r, "path", ""))]
        full = get_openapi(title=app.title, version=app.version, routes=feat_routes)
        # Force all operations under one tag so they group under a single Swagger
        # section — many lazy modules tag routes inconsistently.
        for path_ops in full.get("paths", {}).values():
            for op in path_ops.values():
                if isinstance(op, dict):
                    op["tags"] = [feat.name]
        return {
            "stub_path": feat.path_prefixes[0],
            "paths": full.get("paths", {}),
            "components": {"schemas": full.get("components", {}).get("schemas", {})},
        }

    return router

