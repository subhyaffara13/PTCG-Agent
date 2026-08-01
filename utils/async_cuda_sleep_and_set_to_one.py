
def async_cuda_sleep_and_set_to_one(t):
    device = t.device
    original_stream = torch.cuda.current_stream(device)
    new_stream = torch.cuda.Stream(device)
    new_stream.wait_stream(original_stream)
    with torch.cuda.stream(new_stream):
        torch.cuda._sleep(int(1000 * get_cycles_per_ms()))
        t.fill_(1)
        fut = Future(devices=[device])
        fut.set_result(t)
        return fut

