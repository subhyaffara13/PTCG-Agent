
def _broadcast_object(
    obj: Any,
    src_rank: int,
    group: object = dist.group.WORLD,
    device: torch.device = torch.device("cpu"),
) -> Any:
    r"""
    Broadcasts an object to the given group.

    It will be sending the object if called from the source rank and receiving
    the object otherwise.

    Arguments:
        obj: object to broadcast; only used if called on the source rank.
        src_rank (int): source rank.
        group (``ProcessGroup``, optional): group used for the broadcast
            (default: ``dist.group.WORLD``).
        device (``torch.device``, optional): device to send from or receive
            to (default: ``torch.device("cpu")``).

    Returns:
        The broadcasted object.
    """
    if dist.get_rank() == src_rank:
        # Send the object
        buffer = io.BytesIO()
        torch.save(obj, buffer)
        data = bytearray(buffer.getbuffer())
        length_tensor = torch.LongTensor([len(data)]).to(device)
        data_send_tensor = torch.ByteTensor(data).to(device)
        # pyrefly: ignore [bad-argument-type]
        dist.broadcast(length_tensor, src=src_rank, group=group, async_op=False)
        # pyrefly: ignore [bad-argument-type]
        dist.broadcast(data_send_tensor, src=src_rank, group=group, async_op=False)
    else:
        # Receive the object
        length_tensor = torch.LongTensor([0]).to(device)
        # pyrefly: ignore [bad-argument-type]
        dist.broadcast(length_tensor, src=src_rank, group=group, async_op=False)
        data_recv_tensor = torch.empty(
            [int(length_tensor.item())], dtype=torch.uint8, device=device
        )
        # pyrefly: ignore [bad-argument-type]
        dist.broadcast(data_recv_tensor, src=src_rank, group=group, async_op=False)
        buffer = io.BytesIO(data_recv_tensor.cpu().numpy())
        obj = torch.load(buffer, map_location=device, weights_only=False)
    return obj

