
def test_X22():
    # (c52) /* => p / 2
    #    - (2 p / pi^2) sum( [1 - (-1)^n] cos(n pi x / p) / n^2,
    #                        n = 1..infinity ) */
    # fourier_series(abs(x), x, p);
    #                       p
    # (e52)                      a  = -
    #                       0      2
    #
    #                       %nn
    #                   (2 (- 1)    - 2) p
    # (e53)                a    = ------------------
    #                 %nn         2    2
    #                       %pi  %nn
    #
    # (e54)                     b    = 0
    #                      %nn
    #
    # Time= 5290 msecs
    #            inf           %nn            %pi %nn x
    #            ====       (2 (- 1)    - 2) cos(---------)
    #            \                    p
    #          p  >       -------------------------------
    #            /               2
    #            ====                %nn
    #            %nn = 1                     p
    # (d54)          ----------------------------------------- + -
    #                       2                 2
    #                    %pi
    raise NotImplementedError("Fourier series not supported")

