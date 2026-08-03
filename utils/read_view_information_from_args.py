from typing import Any

def read_view_information_from_args(
    mutable_arg_names: list[str],
    mutable_arg_types: list[torch.Type],
    kwargs: dict[str, Any],
    all_bases: list[Tensor],
):
    """
    This reads the view information added by `write_view_information_to_args` from kwargs, pop them,
    and returns a dict arg_name -> ViewInfo | [ViewInfo](if the input is list). that maps each mutable arg
    to its view information.
    mutable_arg_names: mutable custom operator arg names.
    mutable_arg_types: mutable custom operator arg types.
    kwargs : args of auto_functionalize(custom_op, kwargs)
    """

    def get_arg(name):
        return kwargs.pop(name)

    def read_single_view(prefix):
        base_index = get_arg(f"{prefix}_base_index")
        if base_index is None:
            return None
        elif f"{prefix}_alias" in kwargs:
            get_arg(f"{prefix}_alias")
            return AliasViewInfo(base_index)
        elif f"{prefix}_storage_offset" in kwargs:
            # The view is regenerated using as_strided.
            size = get_arg(f"{prefix}_size")
            stride = get_arg(f"{prefix}_stride")
            storage_offset = get_arg(f"{prefix}_storage_offset")
            return AsStridedViewInfo(base_index, size, stride, storage_offset)
        elif f"{prefix}_slice_dim" in kwargs:
            dim = get_arg(f"{prefix}_slice_dim")
            start = get_arg(f"{prefix}_slice_start")
            end = get_arg(f"{prefix}_slice_end")
            return SliceViewInfo(base_index, dim, start, end)
        else:
            # This means that the argument is the base tensor
            return NotView(base_index)

    args_view_info: dict[str, Any] = {}
    for arg_name, arg_type in zip(mutable_arg_names, mutable_arg_types):
        if library_utils.is_tensorlist_like_type(arg_type):
            length = get_arg(f"_{arg_name}_length")
            if length is None:
                # The whole list is None.
                args_view_info[arg_name] = None
            else:
                args_view_info[arg_name] = [
                    read_single_view(f"_{arg_name}_{i}") for i in range(length)
                ]

        elif library_utils.is_tensor_like_type(arg_type):
            args_view_info[arg_name] = read_single_view(f"_{arg_name}")
        else:
            raise RuntimeError(f"Unsupported type {arg_type}")
    return args_view_info

