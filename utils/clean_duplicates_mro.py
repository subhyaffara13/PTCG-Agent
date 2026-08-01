
def clean_duplicates_mro(
    sequences: list[list[ClassDef]],
    cls: ClassDef,
    context: InferenceContext | None,
) -> list[list[ClassDef]]:
    for sequence in sequences:
        seen = set()
        for node in sequence:
            lineno_and_qname = (node.lineno, node.qname())
            if lineno_and_qname in seen:
                raise DuplicateBasesError(
                    message="Duplicates found in MROs {mros} for {cls!r}.",
                    mros=sequences,
                    cls=cls,
                    context=context,
                )
            seen.add(lineno_and_qname)
    return sequences

