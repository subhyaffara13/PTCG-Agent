
def _run_flat_inference(model, device, flat_batch, batch, flat_indices):
    flat_tensor = torch.cat(flat_batch, dim=0).to(device)
    logits, values = model(x=flat_tensor)
    for j, idx in enumerate(flat_indices):
        batch[idx].logits = logits[j].cpu().tolist()
        batch[idx].value = values[j].item()
        batch[idx].result_event.set()

