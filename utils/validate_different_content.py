
def validate_different_content(v: Union[str, dict, list]) -> str:
    if v in ((), {}, []):
        return ""
    elif isinstance(v, dict) and "text" in v:
        return v["text"]
    elif isinstance(v, list):
        new_v = []
        for item in v:
            if isinstance(item, dict) and "text" in item:
                if item["text"]:
                    new_v.append(item["text"])
            elif isinstance(item, str):
                new_v.append(item)
        return "\n".join(new_v)
    elif isinstance(v, str):
        return v
    raise ValueError("Content must be a string")

