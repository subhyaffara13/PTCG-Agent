from typing import Callable

def _mount_app(
    prefix: str, attr_name: str = "app"
) -> Callable[["FastAPI", object], None]:
    def _register(app: "FastAPI", module: object) -> None:
        app.mount(path=prefix, app=getattr(module, attr_name))

    return _register

