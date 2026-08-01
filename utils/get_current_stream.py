
def get_current_stream(device: torch.device) -> torch.Stream:
    return torch.accelerator.current_stream(device)


def get_current_stream(device: torch.device) -> int:
    stream = torch.accelerator.current_stream(device)
    return register_graph_created_object(
        stream, lambda _, cg: _codegen_current_stream(device, cg)
    )

