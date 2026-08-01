
def wait_until_owners_and_forks_on_rank(
    num_owners: int, num_forks: int, rank: int, timeout: int = 20
) -> None:
    """
    Waits until timeout for num_forks and num_owners to exist on the rank. Used
    to ensure proper deletion of RRefs in tests.
    """
    start = time.time()
    while True:
        num_owners_on_rank, num_forks_on_rank = rpc.rpc_sync(
            worker_name(rank), get_num_owners_and_forks, args=(), timeout=5
        )
        num_owners_on_rank = int(num_owners_on_rank)
        num_forks_on_rank = int(num_forks_on_rank)
        if num_owners_on_rank == num_owners and num_forks_on_rank == num_forks:
            return
        time.sleep(1)
        if time.time() - start > timeout:
            raise ValueError(
                f"Timed out waiting {timeout} sec for {num_owners} owners and {num_forks} forks on rank,"
                f" had {num_owners_on_rank} owners and {num_forks_on_rank} forks"
            )

