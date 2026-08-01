
def _check_outputs(outputs) -> None:
    if any(_is_sparse_any_tensor(t) for t in outputs if isinstance(t, torch.Tensor)):
        # it is easier to call to_dense() on the sparse output than
        # to modify analytical jacobian
        raise ValueError(
            "Sparse output is not supported at gradcheck yet. "
            "Please call to_dense(masked_grad=...) on the output of fn for gradcheck."
        )
    if any(t.layout == torch._mkldnn for t in outputs if isinstance(t, torch.Tensor)):  # type: ignore[attr-defined]
        raise ValueError(
            "MKLDNN output is not supported at gradcheck yet. "
            "Please call to_dense(masked_grad=...) on the output of fn for gradcheck."
        )

