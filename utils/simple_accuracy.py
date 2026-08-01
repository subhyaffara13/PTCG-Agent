
def simple_accuracy(preds, labels):
    warnings.warn(DEPRECATION_WARNING, FutureWarning)
    requires_backends(simple_accuracy, "sklearn")
    return (preds == labels).mean()

