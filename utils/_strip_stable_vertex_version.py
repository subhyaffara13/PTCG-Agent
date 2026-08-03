import re

def _strip_stable_vertex_version(model_name) -> str:
    return re.sub(r"-\d+$", "", model_name)

