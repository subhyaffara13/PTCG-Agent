
def write_test_cpp(cpp_ops: Sequence[str], file_path: str) -> None:
    code = "\n".join(cpp_ops)
    generated = f"""// @lint-ignore-every CLANGTIDY HOWTOEVEN
// AUTO-GENERATED FROM: torchgen/static_runtime/gen_static_runtime_ops.py
#include <gtest/gtest.h>
#include <torch/csrc/jit/runtime/static/impl.h>
#include <torch/torch.h>

#include "test_utils.h"

using namespace caffe2;
using namespace torch;
using namespace torch::jit;
using namespace torch::jit::test;
using c10::IValue;

{code}

"""
    with open(file_path, "w") as f:
        f.write(generated)
    clang_format(file_path)

