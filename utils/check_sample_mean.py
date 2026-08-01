
def check_sample_mean(sample, popmean):
    # Checks for unlikely difference between sample mean and population mean
    prob = stats.ttest_1samp(sample, popmean).pvalue
    assert prob > 0.01

