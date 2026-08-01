
def find_file(filename, levels):
  if os.path.isfile(filename):
    return filename
  else:
    for _ in range(levels):
      filename = '../' + filename
      if os.path.isfile(filename):
        return filename
  return None

