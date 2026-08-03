from typing import Any

def test_torch(string: str) -> None:
    torch = pytest.importorskip("torch")

    views = build_views(string, array_function=torch.rand)
    ein = torch.einsum(string, *views)

    shps = [v.shape for v in views]
    expr = contract_expression(string, *shps, optimize=True)

    opt = expr(*views, backend="torch")
    torch.testing.assert_close(ein, opt)

    # test non-conversion mode
    torch_views = [backends.to_torch(view) for view in views]
    torch_opt = expr(*torch_views)
    assert isinstance(torch_opt, torch.Tensor)
    torch.testing.assert_close(ein, torch_opt)


def test_torch(args, device) -> list[dict[str, Any]]:
    model = load_torch_model(args.model, device)
    return test_torch_latency(
        device,
        model,
        args.model,
        args.batch_sizes,
        args.sequence_lengths,
        args.global_lengths,
        args.test_times,
        args.num_threads,
    )

