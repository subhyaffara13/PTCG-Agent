import uuid

def _as_temp_path(host, path, temppath):
    share = path.split("/")[1]
    temp_file = f"/{share}{temppath}/{uuid.uuid4()}"
    unc = _as_unc_path(host, temp_file)
    return unc

