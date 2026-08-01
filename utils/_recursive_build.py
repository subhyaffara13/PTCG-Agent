
def _recursive_build(
    scalarType: torch.dtype, obj: TensorOrNumberLikeType | TensorSequenceType
):
    if isinstance(obj, Tensor) and obj.numel() == 1:
        return obj.detach().to(dtype=scalarType, device="cpu", copy=True).view(())
    elif isinstance(obj, Tensor):
        # It is invalid to call ".tensor([...])" with a non-scalar tensor in eager mode
        # >>> torch.tensor([torch.randn(2)])
        # ValueError: only one element tensors can be converted to Python scalars
        #
        # But it is possible with a NumPy array
        # >>> torch.tensor([np.random.uniform(size=(2,))]).shape
        # torch.Size([1, 2])
        return obj.detach().to(dtype=scalarType, device="cpu", copy=True)
    elif isinstance(obj, Number):
        # pyrefly: ignore [bad-argument-type]
        return torch.scalar_tensor(obj, dtype=scalarType)

    # seq can be a list of tensors
    seq = obj
    return (
        torch.empty(0)
        if not seq
        else torch.stack([_recursive_build(scalarType, item) for item in seq])
    )

