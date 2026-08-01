
def get_lstm_mod_weights(mod: nn.Module) -> list[torch.Tensor]:
    # TODO(future PR): make more generic, handle everything
    if isinstance(mod, nn.LSTM):
        res = []
        for idx, param_name in enumerate(mod._flat_weights_names):
            if "weight_ih_l" in param_name or "weight_hh_l" in param_name:
                param_value = mod._flat_weights[idx].detach()  # type: ignore[index,union-attr]
                res.append(param_value)
        return res
    else:
        if not isinstance(mod, nnqd.LSTM):
            raise AssertionError(f"type {type(mod)} not handled yet")
        res = []
        for weight_value in mod._all_weight_values:
            res.append(
                weight_value.param.__getstate__()[0][4][0].__getstate__()[0][0]  # type: ignore[index]
            )
            res.append(
                weight_value.param.__getstate__()[0][4][1].__getstate__()[0][0]  # type: ignore[index]
            )
        return res

