
def construct_stacked_leaf(
    tensors: tuple[Tensor, ...] | list[Tensor], name: str
) -> Tensor:
    all_requires_grad = all(t.requires_grad for t in tensors)
    none_requires_grad = all(not t.requires_grad for t in tensors)
    if not all_requires_grad and not none_requires_grad:
        raise RuntimeError(
            f"Expected {name} from each model to have the same .requires_grad"
        )
    result = torch.stack(tensors)
    if all_requires_grad:
        result = result.detach().requires_grad_()
    return result

