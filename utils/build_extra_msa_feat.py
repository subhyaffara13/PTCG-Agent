
def build_extra_msa_feat(batch: dict[str, torch.Tensor]) -> torch.Tensor:
    msa_1hot: torch.LongTensor = nn.functional.one_hot(batch["extra_msa"], 23)
    msa_feat = [
        msa_1hot,
        batch["extra_has_deletion"].unsqueeze(-1),
        batch["extra_deletion_value"].unsqueeze(-1),
    ]
    return torch.cat(msa_feat, dim=-1)

