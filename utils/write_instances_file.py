
def write_instances_file(negotiations, filename):
  contents = ""
  for nego in negotiations:
    contents += str(nego.instance) + "\n"
  pyspiel.write_contents_to_file(filename, "w", contents)

