
def _strip_datapipe_from_name(name: str) -> str:
    return name.replace("IterDataPipe", "").replace("MapDataPipe", "")

