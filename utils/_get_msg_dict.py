
def _get_msg_dict(func_name, *args, **kwargs) -> dict[str, Any]:
    if dist.is_initialized():
        group = kwargs.get("group") or kwargs.get("process_group")
        msg_dict = {
            "func_name": f"{func_name}",
            "pg_name": f"{dist._get_process_group_name(kwargs.get('pg'))}",  # type: ignore[arg-type]
            "backend": f"{dist.get_backend(group)}",
            "world_size": f"{dist.get_world_size()}",
            "group_size": f"{dist.get_world_size(group)}",
            "global_rank": f"{dist.get_rank()}",
            "local_rank": f"{dist.get_rank(group)}",
        }
        if msg_dict["backend"] == "nccl":
            nccl_version = torch.cuda.nccl.version()
            msg_dict["nccl_version"] = ".".join(str(v) for v in nccl_version)
    else:
        msg_dict = {
            "func_name": f"{func_name}",
        }
    return msg_dict


def _get_msg_dict(func_name, *args, **kwargs) -> dict[str, Any]:
    msg_dict = _msg_dict_from_dcp_method_args(*args, **kwargs)
    msg_dict.update(c10d_logger._get_msg_dict(func_name, *args, **kwargs))

    return msg_dict

