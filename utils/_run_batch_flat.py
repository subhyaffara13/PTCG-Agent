
def _run_batch_flat(self, batch, flat_indices, flat_batch):
    flat_tensor = torch.cat(flat_batch, dim=0).to(self.device)
    logits, values = self.model(x=flat_tensor)
    for j, idx in enumerate(flat_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()

