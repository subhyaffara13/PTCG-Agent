
def _post_process_flash_output(out: torch.Tensor, og_size):
    if not out.is_nested and out.size(-1) != og_size:
        out = out[..., 0:og_size]
    return out

