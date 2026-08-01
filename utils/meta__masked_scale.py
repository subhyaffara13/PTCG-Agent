
def meta__masked_scale(self, mask, scale):
    masked_scale = self.new_empty(self.size()).to(
        memory_format=utils.suggest_memory_format(self)
    )
    return masked_scale

