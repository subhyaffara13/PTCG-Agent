
def embedding_override(self, input):
    return torch.empty(*input.shape, self.weight.shape[-1], device="meta")

