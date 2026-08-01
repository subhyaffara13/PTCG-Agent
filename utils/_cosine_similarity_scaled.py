
def _cosine_similarity_scaled(a, b, logit_scale):
    a = a / a.norm(dim=2, keepdim=True).clamp_min(1e-12)
    b = b / b.norm(dim=1, keepdim=True).clamp_min(1e-12)
    logit_scale = logit_scale.exp()
    logits_per_image = logit_scale * torch.bmm(a, b)
    return logits_per_image

