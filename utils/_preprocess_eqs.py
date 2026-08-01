
def _preprocess_eqs(eqs):
    processed_eqs = []
    for eq in eqs:
        processed_eqs.append(eq if isinstance(eq, Equality) else Eq(eq, 0))

    return processed_eqs

