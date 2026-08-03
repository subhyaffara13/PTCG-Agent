from typing import Any

def _create_app_mock() -> mock.MagicMock:
    def get_dict(app: Any, key: str) -> Any:
        return app.__app_dict[key]

    def set_dict(app: Any, key: str, value: Any) -> None:
        app.__app_dict[key] = value

    app = mock.MagicMock(spec=Application)
    app.__app_dict = {}
    app.__getitem__ = get_dict
    app.__setitem__ = set_dict

    app._debug = False
    app.on_response_prepare = Signal(app)
    app.on_response_prepare.freeze()
    return app

