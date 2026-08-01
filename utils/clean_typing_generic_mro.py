
def clean_typing_generic_mro(sequences: list[list[ClassDef]]) -> None:
    """A class can inherit from typing.Generic directly, as base,
    and as base of bases. The merged MRO must however only contain the last entry.
    To prepare for _c3_merge, remove some typing.Generic entries from
    sequences if multiple are present.

    This method will check if Generic is in inferred_bases and also
    part of bases_mro. If true, remove it from inferred_bases
    as well as its entry the bases_mro.

    Format sequences: [[self]] + bases_mro + [inferred_bases]
    """
    bases_mro = sequences[1:-1]
    inferred_bases = sequences[-1]
    # Check if Generic is part of inferred_bases
    for i, base in enumerate(inferred_bases):
        if base.qname() == "typing.Generic":
            position_in_inferred_bases = i
            break
    else:
        return
    # Check if also part of bases_mro
    # Ignore entry for typing.Generic
    for i, seq in enumerate(bases_mro):
        if i == position_in_inferred_bases:
            continue
        if any(base.qname() == "typing.Generic" for base in seq):
            break
    else:
        return
    # Found multiple Generics in mro, remove entry from inferred_bases
    # and the corresponding one from bases_mro
    inferred_bases.pop(position_in_inferred_bases)
    bases_mro.pop(position_in_inferred_bases)

