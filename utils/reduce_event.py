
def reduce_event(event):
    handle = event.ipc_handle()
    return (rebuild_event, (event.device, handle))

