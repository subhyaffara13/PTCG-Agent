
def _run_transformer_inference(model, device, token_batch, zone_batch, scalar_batch, mask_batch, batch, transformer_indices):
    tokens = torch.cat(token_batch, dim=0).to(device)
    zones = torch.cat(zone_batch, dim=0).to(device)
    scalars = torch.cat(scalar_batch, dim=0).to(device)
    masks = torch.cat(mask_batch, dim=0).to(device)
    logits, values = model(x=None, token_ids=tokens, zone_ids=zones, scalars=scalars, padding_mask=masks)
    for j, idx in enumerate(transformer_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()

