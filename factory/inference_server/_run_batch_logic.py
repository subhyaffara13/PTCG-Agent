import torch

def _prepare_batch_data(batch, state_to_card_tokens, state_to_tensor):
    token_batch, zone_batch, scalar_batch, mask_batch = [], [], [], []
    flat_batch = []
    transformer_indices = []
    flat_indices = []
    use_transformer = state_to_card_tokens is not None
    for i, req in enumerate(batch):
        if use_transformer:
            try:
                t, z, s, m = state_to_card_tokens(req.state_data)
                if t is not None:
                    token_batch.append(t); zone_batch.append(z)
                    scalar_batch.append(s); mask_batch.append(m)
                    transformer_indices.append(i)
                    continue
            except Exception:
                pass
        if state_to_tensor is not None:
            try:
                flat_t = state_to_tensor(req.state_data)
                if flat_t is not None:
                    flat_batch.append(flat_t)
                    flat_indices.append(i)
                    continue
            except Exception:
                pass
        req.logits = None; req.value = 0.0; req.result_event.set()
    return token_batch, zone_batch, scalar_batch, mask_batch, flat_batch, transformer_indices, flat_indices

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

def _run_flat_inference(model, device, flat_batch, batch, flat_indices):
    flat_tensor = torch.cat(flat_batch, dim=0).to(device)
    logits, values = model(x=flat_tensor)
    for j, idx in enumerate(flat_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()

def _set_default_results(batch):
    for req in batch:
        req.logits = None
        req.value = 0.0
        req.result_event.set()
