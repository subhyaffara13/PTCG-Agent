
def make_atom14_masks_np(batch: dict[str, torch.Tensor]) -> dict[str, np.ndarray]:
    batch = tree_map(lambda n: torch.tensor(n, device=batch["aatype"].device), batch, np.ndarray)
    out = tensor_tree_map(lambda t: np.array(t), make_atom14_masks(batch))
    return out

