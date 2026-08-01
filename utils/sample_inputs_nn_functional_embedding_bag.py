
def sample_inputs_nn_functional_embedding_bag(
    op_info, device, dtype, requires_grad, **kwargs
):
    for generate_per_sample_weight in (True, False):
        for mode in ("sum", "mean", "max"):
            # per_sample_weights is only supported for mode='sum'
            if mode != "sum" and generate_per_sample_weight:
                continue

            NUM_EMBEDDINGS = 10
            EMBEDDING_DIM = 32
            weight = torch.randn(
                NUM_EMBEDDINGS, EMBEDDING_DIM, dtype=dtype, device=device
            )

            njt = torch.nested.nested_tensor(
                [
                    torch.randint(0, NUM_EMBEDDINGS, size=(2,)),
                    torch.randint(0, NUM_EMBEDDINGS, size=(3,)),
                    torch.randint(0, NUM_EMBEDDINGS, size=(4,)),
                ],
                layout=torch.jagged,
                dtype=torch.int64,
                device=device,
            )

            per_sample_weights = None
            if generate_per_sample_weight:
                per_sample_weights = torch.randn_like(njt, dtype=dtype)

            # NB: the OpInfo entry for embedding_bag expects weight first so the gradients
            # can be checked
            yield SampleInput(
                weight,
                args=(njt,),
                kwargs={
                    "mode": mode,
                    "per_sample_weights": per_sample_weights,
                },
            )

