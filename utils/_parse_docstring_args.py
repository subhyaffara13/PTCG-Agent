
def _parse_docstring_args(doc_str: str) -> dict[str, str]:
  """Parses parameters from `Args:` section of a function docstring.
  Assumes Google style docstrings. Returns a dictionary with
  keys representing argument names and values representing descriptions.
  Each description has lines starting with 4 spaces.
  """
  lines = doc_str.split("\n")

  # Get lines with the parameter names
  inds = [i for i, l in enumerate(lines) if l.startswith("  ") and not l.startswith("    ")]
  inds.append(len(lines))
  out = dict()

  # Parse each argument
  for i in range(len(inds)-1):
    start, end = inds[i], inds[i+1]

    # Process first line for the description
    first_colon = lines[start].find(":")
    name = lines[start][:first_colon].strip()
    desc = [" "*4 + lines[start][first_colon+1:].strip()]

    # Append remaining description lines
    for j in range(start+1, end):
      desc.append(lines[j])

    out[name] = "\n".join(desc)
  return out

