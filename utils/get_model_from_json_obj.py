
def get_model_from_json_obj(json_object: dict) -> Optional[str]:
    body = json_object.get("body", {}) or {}
    model = body.get("model")

    return model

