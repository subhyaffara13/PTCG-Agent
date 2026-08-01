
def prepare_fw_with_masks(fn):
    def fw_with_masks(*args):
        fw_out = fn(*args)
        return fw_out, [
            bool(isinstance(ret, torch.Tensor) and ret.requires_grad) for ret in fw_out
        ]

    return fw_with_masks

