
def _serve_run_batch(self, batch):
    try:
        self._run_batch(batch)
    except Exception as e:
        logger.error(f"InferenceServer batch failed: {e}")
        for req in batch:
            req.logits = None
            req.value = 0.0
            req.result_event.set()
    self._stats["total_requests"] += len(batch)
    self._stats["total_batches"] += 1
    self._stats["avg_batch_size"] = self._stats["total_requests"] / max(1, self._stats["total_batches"])

