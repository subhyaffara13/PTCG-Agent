
def meta_pixel_shuffle(self, upscale_factor):
    if not (
        len(self.shape) > 2 and self.shape[-3] % (upscale_factor * upscale_factor) == 0
    ):
        raise AssertionError(
            f"Invalid input shape for pixel_shuffle: {self.shape} with upscale_factor = {upscale_factor}"
        )

    def is_channels_last(ten):
        return torch._prims_common.suggest_memory_format(ten) == torch.channels_last

    def pick_memory_format():
        if is_channels_last(self):
            if device_hint(self) == "cuda":
                return torch.contiguous_format
            else:
                return torch.channels_last
        elif self.is_contiguous(memory_format=torch.contiguous_format):
            return torch.contiguous_format
        elif self.is_contiguous(memory_format=torch.preserve_format):
            return torch.preserve_format

    C = self.shape[-3] // (upscale_factor * upscale_factor)
    Hr = self.shape[-2] * upscale_factor
    Wr = self.shape[-1] * upscale_factor
    out_shape = (*self.shape[:-3], C, Hr, Wr)

    out = self.new_empty(out_shape)
    out = out.to(memory_format=pick_memory_format())  # type: ignore[call-overload]
    return out

