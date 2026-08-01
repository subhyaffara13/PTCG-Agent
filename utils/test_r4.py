
def test_R4():
# Macsyma indefinite sum test case:
#(c15) /* Check whether the full Gosper algorithm is implemented
#   => 1/2^(n + 1) binomial(n, k - 1) */
#closedform(indefsum(binomial(n, k)/2^n - binomial(n + 1, k)/2^(n + 1), k));
#Time= 2690 msecs
#                      (- n + k - 1) binomial(n + 1, k)
#(d15)               - --------------------------------
#                                     n
#                                   2 2  (n + 1)
#
#(c16) factcomb(makefact(%));
#Time= 220 msecs
#                                 n!
#(d16)                     ----------------
#                                n
#                          2 k! 2  (n - k)!
# Might be possible after fixing https://github.com/sympy/sympy/pull/1879
    raise NotImplementedError("Indefinite sum not supported")

