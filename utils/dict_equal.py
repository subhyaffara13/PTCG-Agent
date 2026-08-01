
def dict_equal(dic1, dic2):
  return all([dic1[a] == dic2[a] for a in dic1]) and all(
      [dic1[a] == dic2[a] for a in dic2]
  )

