
def _match_archetype(deck, arch_data):
    deck_strs = [str(c) for c in deck]
    best_arch = "utility"; max_matches = 0
    for arch, config in arch_data.items():
        sigs = config.get("signature_cards", [])
        matches = sum(1 for c in deck_strs if c in sigs)
        if matches > max_matches: max_matches = matches; best_arch = arch
    return best_arch

