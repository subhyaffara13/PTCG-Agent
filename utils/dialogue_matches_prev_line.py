
def dialogue_matches_prev_line(line1, line2):
  """Checks if the dialogue matches the previous line's."""
  parts1 = line1.split(" ")
  parts2 = line2.split(" ")
  for i in range(6, min(len(parts1), len(parts2))):
    if parts1[i] == "YOU:" or parts1[i] == "THEM:":
      if parts1[i] == "YOU:" and parts2[i] != "THEM:":
        return False
      if parts1[i] == "THEM:" and parts2[i] != "YOU:":
        return False
    elif parts1[i] != parts2[i]:
      return False
    if parts1[i] == "<selection>":
      break
  return True

