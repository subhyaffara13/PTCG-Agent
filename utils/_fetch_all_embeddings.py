
def _fetch_all_embeddings(model):
    """Fetches Embedding and EmbeddingBag modules from the model"""
    embedding_modules = []
    stack = [model]
    while stack:
        module = stack.pop()
        for _, child in module.named_children():
            fqn_name = module_to_fqn(model, child)
            if type(child) in SUPPORTED_MODULES:
                embedding_modules.append((fqn_name, child))
            else:
                stack.append(child)
    return embedding_modules

