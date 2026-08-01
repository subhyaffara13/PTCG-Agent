
def _removechars(s, chars):
  return s.translate(str.maketrans(dict.fromkeys(chars)))

