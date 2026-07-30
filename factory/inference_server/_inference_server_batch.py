import time, torch
from . import Empty, logger

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

def _run_batch_transformer(self, batch, transformer_indices, token_batch, zone_batch, scalar_batch, mask_batch):
    tokens = torch.cat(token_batch, dim=0).to(self.device)
    zones = torch.cat(zone_batch, dim=0).to(self.device)
    scalars = torch.cat(scalar_batch, dim=0).to(self.device)
    masks = torch.cat(mask_batch, dim=0).to(self.device)
    logits, values = self.model(x=None, token_ids=tokens, zone_ids=zones, scalars=scalars, padding_mask=masks)
    for j, idx in enumerate(transformer_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()

def _run_batch_flat(self, batch, flat_indices, flat_batch):
    flat_tensor = torch.cat(flat_batch, dim=0).to(self.device)
    logits, values = self.model(x=flat_tensor)
    for j, idx in enumerate(flat_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()
