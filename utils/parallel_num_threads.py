
def parallel_num_threads() -> int:
    threads = config.cpp.threads
    if threads < 1:
        threads = torch.get_num_threads()
    return threads

