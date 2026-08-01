
def _print_confusion_report(label: str, metrics: dict, wrong: list) -> None:
    """Print the confusion matrix report to stdout."""
    print("\n")  # noqa: T201
    print("=" * 70)  # noqa: T201
    print(f"  {label}")  # noqa: T201
    print("=" * 70)  # noqa: T201
    print(f"  Total cases:  {metrics['total']}")  # noqa: T201
    print(f"  Correct:      {metrics['tp'] + metrics['tn']}")  # noqa: T201
    print(f"  Wrong:        {metrics['fp'] + metrics['fn']}")  # noqa: T201
    print()  # noqa: T201
    print(f"  TP (correctly blocked):  {metrics['tp']}")  # noqa: T201
    print(f"  TN (correctly allowed):  {metrics['tn']}")  # noqa: T201
    print(f"  FP (wrongly blocked):    {metrics['fp']}")  # noqa: T201
    print(f"  FN (wrongly allowed):    {metrics['fn']}")  # noqa: T201
    print()  # noqa: T201
    print(f"  Precision:  {metrics['precision']:.1%}")  # noqa: T201
    print(f"  Recall:     {metrics['recall']:.1%}")  # noqa: T201
    print(f"  F1:         {metrics['f1']:.1%}")  # noqa: T201
    print(f"  Accuracy:   {metrics['accuracy']:.1%}")  # noqa: T201
    print()  # noqa: T201
    print(f"  Latency p50:  {metrics['p50']:.1f}ms")  # noqa: T201
    print(f"  Latency p95:  {metrics['p95']:.1f}ms")  # noqa: T201
    print(f"  Latency avg:  {metrics['avg_lat']:.1f}ms")  # noqa: T201
    print()  # noqa: T201
    if wrong:
        print("WRONG ANSWERS:")  # noqa: T201
        for line in wrong:
            print(line)  # noqa: T201
    else:
        print("ALL CASES CORRECT")  # noqa: T201
    print("=" * 70)  # noqa: T201

