from typing import Callable

def get_owning_type(t: CType) -> tuple[CType, Callable[[str], str]]:
    if t == BaseCType(tensorListT):
        return VectorCType(BaseCType(tensorT)), lambda x: f"{x}.vec()"
    if t == BaseCType(iTensorListRefT):
        return VectorCType(BaseCType(tensorT)), lambda x: f"{{{x}.begin(), {x}.end()}}"
    # There are technically other non-owning types out there (like IntArrayRef),
    # but functionalization only actually cares about the ones involving tensors.
    return t, lambda x: x

