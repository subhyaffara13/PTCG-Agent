
def multi_replica_reload_events(
    commit_sha: str,
    host: str,
    subdomain: str,
    replica_hashes: list[str],
    token: str | None,
    max_retries: int = 10,
) -> Iterator[
    MultiReplicaStreamWarning | MultiReplicaStreamEvent | MultiReplicaStreamReplicaHash | MultiReplicaStreamFullMatch
]:
    clients = [
        ReloadClient(
            host=host,
            subdomain=subdomain,
            replica_hash=hash,
            token=token,
        )
        for hash in replica_hashes
    ]

    first_client_events: dict[int, ApiGetReloadEventSourceData] = {}
    for client_index, client in enumerate(clients):
        if len(clients) > 1:
            yield {"kind": "replicaHash", "hash": client.replica_hash}

        retries = 0
        while isinstance((events := client.get_reload(commit_sha)), int):
            if (retries := retries + 1) > max_retries:
                raise Exception("Too many retries reached")
            if (status_code := events) not in (200, 204):
                raise Exception(f"Unexpected {status_code=} on `ReloadClient.get_reload`")
            subject = "reloadId" if status_code == 204 else "replica"
            yield {"kind": "warning", "message": f"Retrying on unexpected {subject} not found"}
            time.sleep(2)

        full_match = True
        replay: deque[ApiGetReloadEventSourceData] = deque()
        for event_index, event in enumerate(events):
            if client_index == 0:
                first_client_events[event_index] = event
            elif full_match := full_match and first_client_events.get(event_index) == event:
                replay.append(event)
                continue
            while replay:
                yield {"kind": "event", "event": replay.popleft()}
            yield {"kind": "event", "event": event}

        if client_index > 0 and full_match:
            yield {"kind": "fullMatch"}

