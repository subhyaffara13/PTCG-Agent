
def module_inputs_torch_nn_Embedding(module_info, device, dtype, requires_grad, training, **kwargs):
    make_empty = partial(torch.empty, device=device, dtype=torch.long, requires_grad=False)
    return [
        ModuleInput(
            constructor_input=FunctionInput(num_embeddings=4, embedding_dim=3),
            forward_input=FunctionInput(make_empty(2, 3).random_(4))
        ),
        ModuleInput(
            constructor_input=FunctionInput(num_embeddings=4, embedding_dim=3),
            forward_input=FunctionInput(make_empty(1, 512).random_(4).expand(7, 512)),
            desc='discontiguous'
        ),
    ]

