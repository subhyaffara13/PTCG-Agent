
def test_callback_num_times():
    # Super-simple micro-benchmarking related to PR #2919.
    # Example runtimes (Intel Xeon 2.2GHz, fully optimized):
    #   num_millions  1, repeats  2:  0.1 secs
    #   num_millions 20, repeats 10: 11.5 secs
    one_million = 1000000
    num_millions = 1  # Try 20 for actual micro-benchmarking.
    repeats = 2  # Try 10.
    rates = []
    for rep in range(repeats):
        t0 = time.time()
        m.callback_num_times(lambda: None, num_millions * one_million)
        td = time.time() - t0
        rate = num_millions / td if td else 0
        rates.append(rate)
        if not rep:
            print()
        print(
            f"callback_num_times: {num_millions:d} million / {td:.3f} seconds = {rate:.3f} million / second"
        )
    if len(rates) > 1:
        print("Min    Mean   Max")
        print(f"{min(rates):6.3f} {sum(rates) / len(rates):6.3f} {max(rates):6.3f}")

