
def rebuild_event(device, handle):
    return torch.cuda.Event.from_ipc_handle(device, handle)

