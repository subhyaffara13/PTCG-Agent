
def dummy_backend():
    db = types.ModuleType("pandas_dummy_backend")
    setattr(db, "plot", lambda *args, **kwargs: "used_dummy")
    return db

