
def gen_all_vmap_plumbing(native_functions: Sequence[NativeFunction]) -> str:
    body = "\n".join(list(mapMaybe(ComputeBatchRulePlumbing(), native_functions)))
    return f"""
#pragma once
#include <ATen/Operators.h>
#include <ATen/functorch/PlumbingHelper.h>

namespace at {{ namespace functorch {{

{body}

}}}} // namespace at::functorch
"""

