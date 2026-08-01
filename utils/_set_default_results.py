
def _set_default_results(batch):
    for req in batch:
        req.logits = None
        req.value = 0.0
        req.result_event.set()

