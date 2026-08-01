
def call_rpc_torchscript_with_record_function(
    dst_worker_name: str, block: str
) -> Tensor:
    fut = rpc.rpc_async(
        dst_worker_name, script_add_ones_with_record_function, (torch.tensor(1), block)
    )
    return fut.wait()

