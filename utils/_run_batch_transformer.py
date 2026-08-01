
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

