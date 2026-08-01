
def is_explicit_any(typ: AnyType) -> bool:
    # Originally I wanted to count as explicit anything derived from an explicit any, but that
    # seemed too strict in some testing.
    # return (typ.type_of_any == TypeOfAny.explicit
    #         or (typ.source_any is not None and typ.source_any.type_of_any == TypeOfAny.explicit))
    # Important question: what should we do with source_any stuff? Does that count?
    # And actually should explicit anys count at all?? Maybe not!
    return typ.type_of_any == TypeOfAny.explicit

