
def get_ltc_helper_fns() -> str:
    return """\
at::Tensor to_meta(const at::Tensor& tensor) {
  // undefined tensors can't be converted to the meta device, since they don't have sizes/strides
  if (!tensor.defined()) return tensor;
  auto out = at::native::empty_strided_meta_symint(tensor.sym_sizes(), tensor.sym_strides(), \
/*dtype=*/tensor.scalar_type(), /*layout=*/tensor.layout(), \
/*device=*/c10::Device(c10::kMeta), /*pin_memory=*/std::nullopt);
  // needs to handle wrapped numbers, so dtype promotion works properly.
  if (tensor.unsafeGetTensorImpl()->is_wrapped_number()) {
    out.unsafeGetTensorImpl()->set_wrapped_number(true);
  }
  return out;
}
std::optional<at::Tensor> to_meta(const std::optional<at::Tensor>& tensor) {
  if (tensor.has_value()) {
    return to_meta(*tensor);
  }
  return std::nullopt;
}

std::vector<at::Tensor> to_meta(at::ITensorListRef t_list) {
  std::vector<at::Tensor> outs;
  outs.reserve(t_list.size());
  for (const auto& tensor : t_list) {
    outs.push_back(to_meta(tensor));
  }
  return outs;
}
"""

