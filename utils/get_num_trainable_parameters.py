
def get_num_trainable_parameters(self) -> int:
    """
    Get the number of trainable parameters.
    """
    return sum(p.numel() for p in self.model.parameters() if p.requires_grad)

