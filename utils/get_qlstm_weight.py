
def get_qlstm_weight(mod: nn.Module) -> list[torch.Tensor]:
    res = []
    for weight_value in mod._all_weight_values:  # type: ignore[union-attr]
        res.append(weight_value.param.__getstate__()[0][4][0].__getstate__()[0][0])
        res.append(weight_value.param.__getstate__()[0][4][1].__getstate__()[0][0])
    return res

