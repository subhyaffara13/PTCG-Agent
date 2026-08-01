
def attach_lazy_features(app: "FastAPI") -> None:
    app.include_router(_make_warmup_router(app))
    app.add_middleware(LazyFeatureMiddleware, fastapi_app=app)

