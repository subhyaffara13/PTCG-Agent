import re

def doc_to_help(doc: str) -> str:
  """Takes a __doc__ string and reformats it as help."""

  # Get rid of starting and ending white space. Using lstrip() or even
  # strip() could drop more than maximum of first line and right space
  # of last line.
  doc = doc.strip()

  # Get rid of all empty lines.
  whitespace_only_line = re.compile('^[ \t]+$', re.M)
  doc = whitespace_only_line.sub('', doc)

  # Cut out common space at line beginnings.
  doc = trim_docstring(doc)

  # Just like this module's comment, comments tend to be aligned somehow.
  # In other words they all start with the same amount of white space.
  # 1) keep double new lines;
  # 2) keep ws after new lines if not empty line;
  # 3) all other new lines shall be changed to a space;
  # Solution: Match new lines between non white space and replace with space.
  doc = re.sub(r'(?<=\S)\n(?=\S)', ' ', doc, flags=re.M)

  return doc

