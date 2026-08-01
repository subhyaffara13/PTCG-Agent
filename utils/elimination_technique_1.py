
def elimination_technique_1(gens, rels, identity):
    rels = rels[:]
    # the shorter relators are examined first so that generators selected for
    # elimination will have shorter strings as equivalent
    rels.sort()
    gens = gens[:]
    redundant_gens = {}
    redundant_rels = []
    used_gens = set()
    # examine each relator in relator list for any generator occurring exactly
    # once
    for rel in rels:
        # don't look for a redundant generator in a relator which
        # depends on previously found ones
        contained_gens = rel.contains_generators()
        if any(g in contained_gens for g in redundant_gens):
            continue
        contained_gens = list(contained_gens)
        contained_gens.sort(reverse = True)
        for gen in contained_gens:
            if rel.generator_count(gen) == 1 and gen not in used_gens:
                k = rel.exponent_sum(gen)
                gen_index = rel.index(gen**k)
                bk = rel.subword(gen_index + 1, len(rel))
                fw = rel.subword(0, gen_index)
                chi = bk*fw
                redundant_gens[gen] = chi**(-1*k)
                used_gens.update(chi.contains_generators())
                redundant_rels.append(rel)
                break
    rels = [r for r in rels if r not in redundant_rels]
    # eliminate the redundant generators from remaining relators
    rels = [r.eliminate_words(redundant_gens, _all = True).identity_cyclic_reduction() for r in rels]
    rels = list(set(rels))
    try:
        rels.remove(identity)
    except ValueError:
        pass
    gens = [g for g in gens if g not in redundant_gens]
    return gens, rels

