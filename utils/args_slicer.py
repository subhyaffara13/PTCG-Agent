
def args_slicer(args, bdims):
  slicers = map(slicer, args, bdims)
  return lambda i: [sl(i) for sl in slicers]

