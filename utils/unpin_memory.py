
def unpin_memory(data_ptr: int) -> None:
    succ = int(torch.cuda.cudart().cudaHostUnregister(data_ptr))
    if succ != 0:
        raise AssertionError(f"Unpinning shared memory failed with error-code: {succ}")

