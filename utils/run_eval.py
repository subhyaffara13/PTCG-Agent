
def run_eval() -> Tuple[int, int, List[dict]]:
    """
    Run the evaluation suite.

    Returns:
        Tuple of (passed, total, failures)
    """
    # Create router with default config
    mock_router = MagicMock()
    router = ComplexityRouter(
        model_name="eval-router",
        litellm_router_instance=mock_router,
    )

    passed = 0
    total = len(EVAL_CASES)
    failures = []

    print("=" * 70)
    print("COMPLEXITY ROUTER EVALUATION")
    print("=" * 70)
    print()

    for i, case in enumerate(EVAL_CASES, 1):
        tier, score, signals = router.classify(case.prompt, case.system_prompt)

        # Check if pass
        is_exact_match = tier == case.expected_tier
        is_acceptable = (
            case.acceptable_tiers is not None and tier in case.acceptable_tiers
        )
        is_pass = is_exact_match or is_acceptable

        if is_pass:
            passed += 1
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
            failures.append(
                {
                    "case": i,
                    "description": case.description,
                    "prompt": (
                        case.prompt[:80] + "..."
                        if len(case.prompt) > 80
                        else case.prompt
                    ),
                    "expected": case.expected_tier.value,
                    "actual": tier.value,
                    "score": round(score, 3),
                    "signals": signals,
                    "acceptable": (
                        [t.value for t in case.acceptable_tiers]
                        if case.acceptable_tiers
                        else None
                    ),
                }
            )

        # Print result
        print(f"[{i:2d}] {status} | {case.description}")
        print(
            f"     Expected: {case.expected_tier.value:10s} | Got: {tier.value:10s} | Score: {score:+.3f}"
        )
        if signals:
            print(f"     Signals: {', '.join(signals)}")
        if not is_pass:
            print(f"     Prompt: {case.prompt[:60]}...")
        print()

    # Summary
    print("=" * 70)
    print(f"RESULTS: {passed}/{total} passed ({100*passed/total:.1f}%)")
    print("=" * 70)

    if failures:
        print("\nFAILURES:")
        print("-" * 70)
        for f in failures:
            print(f"Case {f['case']}: {f['description']}")
            print(
                f"  Expected: {f['expected']}, Got: {f['actual']} (score: {f['score']})"
            )
            print(f"  Signals: {f['signals']}")
            if f["acceptable"]:
                print(f"  Acceptable: {f['acceptable']}")
            print()

    return passed, total, failures

