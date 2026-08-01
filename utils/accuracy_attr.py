
def accuracy_attr(accuracy) -> hlo.ResultAccuracyAttr | None:
  if accuracy is None:
    return None
  elif isinstance(accuracy, AccuracyMode):
    return hlo.ResultAccuracyAttr.get(0.0, 0.0, int(0), str(accuracy.name))
  elif isinstance(accuracy, Tolerance):
    return hlo.ResultAccuracyAttr.get(
        atol=accuracy.atol,
        rtol=accuracy.rtol,
        ulps=accuracy.ulps,
        mode='TOLERANCE',
    )
  raise NotImplementedError(f"Accuracy {accuracy} not supported")

