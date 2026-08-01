
def get_spec_name(label):
  """Converts the label of bazel rule to the name of podspec."""
  assert label.startswith("//absl/"), "{} doesn't start with //absl/".format(
      label)
  # e.g. //absl/apple/banana -> abseil/apple/banana
  return "abseil/" + label[7:]

