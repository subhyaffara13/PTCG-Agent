
def _serve_collect_batch(self):
    batch = []
    deadline = time.monotonic() + self.max_wait_s
    while len(batch) < self.batch_size:
        remaining = max(0.001, deadline - time.monotonic())
        try:
            request = self.request_queue.get(timeout=remaining)
            batch.append(request)
        except Empty:
            break
    return batch

