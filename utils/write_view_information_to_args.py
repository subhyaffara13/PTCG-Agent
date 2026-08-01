
def write_view_information_to_args(
    mutable_arg_names: list[str],
    mutable_arg_types: list[torch.Type],
    kwargs: dict[str, Any],
    arg_to_base_index: dict[str, Any],
):
    """
    This function writes the view information into kwargs. It reads mutable_args from kwargs.
    and uses arg_to_base_index and tensor information to write ViewInfo into kwargs.
    mutable_arg_names: mutable custom operator arg names.
    mutable_arg_types: mutable custom operator arg types.
    kwargs: the original custom operator args.
    arg_to_base_index: maps mutable_arg_name to int | [int] that refers to the base tensor that
                       corresponds to the input tensor
    """

    def write_single_view(prefix: str, tensor: Tensor, base_index: int):
        if f"{prefix}_base_index" in kwargs:
            raise AssertionError(f"{prefix}_base_index already in kwargs")
        if f"{prefix}_size" in kwargs:
            raise AssertionError(f"{prefix}_size already in kwargs")
        if f"{prefix}_stride" in kwargs:
            raise AssertionError(f"{prefix}_stride already in kwargs")
        if f"{prefix}_storage_offset" in kwargs:
            raise AssertionError(f"{prefix}_storage_offset already in kwargs")

        if f"{prefix}_slice_dim" in kwargs:
            raise AssertionError(f"{prefix}_slice_dim already in kwargs")
        if f"{prefix}_slice_start" in kwargs:
            raise AssertionError(f"{prefix}_slice_start already in kwargs")
        if f"{prefix}_slice_end" in kwargs:
            raise AssertionError(f"{prefix}_slice_end already in kwargs")

        def use_as_strided(tensor):
            kwargs[f"{prefix}_size"] = tensor.size()
            kwargs[f"{prefix}_stride"] = tensor.stride()
            kwargs[f"{prefix}_storage_offset"] = tensor.storage_offset()

        def use_slice(dim, start, end):
            kwargs[f"{prefix}_slice_dim"] = dim
            kwargs[f"{prefix}_slice_start"] = start
            kwargs[f"{prefix}_slice_end"] = end

        def use_alias():
            kwargs[f"{prefix}_alias"] = True

        # The start if the function
        if tensor is None:
            kwargs[f"{prefix}_base_index"] = None
        else:
            base = get_base(tensor)
            kwargs[f"{prefix}_base_index"] = base_index
            if base is None:
                # no need to add anything else other than _base_index
                return
            elif is_alias(base, tensor):
                use_alias()
            elif (slice_info := try_use_slice(base, tensor)) is not None:
                use_slice(*slice_info)
            else:
                use_as_strided(tensor)

    for arg_name, arg_type in zip(mutable_arg_names, mutable_arg_types):
        arg = kwargs[arg_name]
        if library_utils.is_tensorlist_like_type(arg_type):
            if arg is None:
                kwargs[f"_{arg_name}_length"] = None
            else:
                kwargs[f"_{arg_name}_length"] = len(arg)
                for i, elem in enumerate(arg):
                    write_single_view(
                        f"_{arg_name}_{i}", elem, arg_to_base_index[arg_name][i]
                    )

        elif library_utils.is_tensor_like_type(arg_type):
            write_single_view(
                f"_{arg_name}",
                kwargs[arg_name],
                arg_to_base_index.get(arg_name),  # type: ignore[arg-type]
            )
        else:
            raise RuntimeError(f"Unsupported type {arg_type}")

