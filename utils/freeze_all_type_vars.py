
def freeze_all_type_vars(member_type: Type) -> None:
    member_type.accept(FreezeTypeVarsVisitor())

