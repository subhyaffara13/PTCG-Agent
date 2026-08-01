
def categorical_lddt(logits, bins=50):
    # Logits are ..., 37, bins.
    return EsmCategoricalMixture(logits, bins=bins).mean()

