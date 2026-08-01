
def unique_id():
    return torch._C._nccl_unique_id()


def unique_id(name: str, with_uuid: bool = False) -> str:
    ret = f"{name}_{next(_unique_id_counter)}"
    if with_uuid:
        ret += f"_{uuid.uuid4()}".replace("-", "_")
    return ret

