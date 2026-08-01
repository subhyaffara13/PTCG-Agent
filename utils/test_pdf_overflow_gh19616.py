
def test_pdf_overflow_gh19616():
    # Confirm that gh19616 (intermediate over/underflows in PDF) is resolved
    # Reference value from R GeneralizedHyperbolic library
    # library(GeneralizedHyperbolic)
    # options(digits=16)
    # jitter = 1e-3
    # dnig(1, a=2**0.5 / jitter**2, b=1 / jitter**2)
    jitter = 1e-3
    Z = stats.norminvgauss(2**0.5 / jitter**2, 1 / jitter**2, loc=0, scale=1)
    assert_allclose(Z.pdf(1.0), 282.0948446666433)

