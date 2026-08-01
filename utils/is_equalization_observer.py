
def is_equalization_observer(
    observer: nn.Module,
) -> TypeIs[_InputEqualizationObserver | _WeightEqualizationObserver]:
    return isinstance(
        observer, (_InputEqualizationObserver, _WeightEqualizationObserver)
    )

