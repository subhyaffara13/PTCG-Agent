
def _obj_from_dict(dict_val: dict[str, Any]) -> JsProxy:
    return to_js(dict_val, dict_converter=js.Object.fromEntries)


def _obj_from_dict(dict_val: dict[str, Any]) -> JsProxy:
    return to_js(dict_val, dict_converter=js.Object.fromEntries)

