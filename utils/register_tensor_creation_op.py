
def register_tensor_creation_op(op):
    @_sharded_op_impl(op)
    def tensor_creation_op(types, args=(), kwargs=None, pg=None):
        """
        Handles ``__torch_function__`` dispatch for tensor creation ops that
        takes a ShardedTensor as argument, such as ``torch.zeros_like`` or
        ``torch.full_like``.
        """
        creation_op = tensor_like_creation_op_map.get(op)
        if creation_op is None:
            raise RuntimeError(f"Tensor creation {op} not supported!")
        if kwargs is None:
            kwargs = {}

        # pyrefly: ignore [bad-index]
        st = args[0]

        new_st = creation_op(st.sharding_spec(), st.size(), *args[1:], **kwargs)  # type: ignore[operator]
        return new_st

