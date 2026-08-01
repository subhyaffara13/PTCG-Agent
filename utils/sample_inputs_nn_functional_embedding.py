
def sample_inputs_nn_functional_embedding(
    op_info, device, dtype, requires_grad, **kwargs
):
    indices = torch.nested.nested_tensor(
        [
            torch.tensor([0, 2, 1, 3]),
            torch.tensor([4, 2, 1]),
            torch.tensor([6, 7, 5, 2, 4]),
        ],
        layout=torch.jagged,
        dtype=torch.int64,
        device=device,
    )

    NUM_EMBEDDINGS = 20
    EMBEDDING_DIM = 32
    weight = torch.randn(NUM_EMBEDDINGS, EMBEDDING_DIM, device=device, dtype=dtype)

    # NB: the OpInfo entry for embedding_bag expects weight first so the gradients
    # can be checked
    yield SampleInput(
        _clone(weight).requires_grad_(),
        args=(indices,),
    )

    yield SampleInput(
        _clone(weight).requires_grad_(),
        args=(indices,),
        kwargs={"padding_idx": 1},
    )

