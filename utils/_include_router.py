from typing import Callable

def _include_router(attr_name: str = "router") -> Callable[["FastAPI", object], None]:
    def _register(app: "FastAPI", module: object) -> None:
        app.include_router(getattr(module, attr_name))

    return _register

