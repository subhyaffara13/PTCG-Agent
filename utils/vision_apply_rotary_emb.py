
def vision_apply_rotary_emb(
    query: torch.Tensor,
    key: torch.Tensor,
    freqs_ci: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    query_ = torch.view_as_complex(query.float().reshape(*query.shape[:-1], -1, 2))
    key_ = torch.view_as_complex(key.float().reshape(*key.shape[:-1], -1, 2))
    freqs_ci = reshape_for_broadcast(freqs_ci=freqs_ci, query=query_)  # freqs_ci[:,:,None,:]
    freqs_ci = freqs_ci.to(query_.device)
    query_out = torch.view_as_real(query_ * freqs_ci).flatten(3)
    key_out = torch.view_as_real(key_ * freqs_ci).flatten(3)
    return query_out.type_as(query), key_out.type_as(key)  # but this drops to 8e-3

