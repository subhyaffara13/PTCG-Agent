
def test_latency(args, device) -> list[dict[str, Any]]:
    if args.engine == "onnxruntime":
        return test_ort(args, device)

    return test_torch(args, device)

