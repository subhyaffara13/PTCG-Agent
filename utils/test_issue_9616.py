from typing import Union

def test_issue_9616():
    assert dumeq(solveset(sinh(x) + tanh(x) - 1, x), Union(
        ImageSet(Lambda(n, 2*n*I*pi + log(sqrt(2)/2 + sqrt(-S.Half + sqrt(2)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi - atan(sqrt(2)*sqrt(S.Half + sqrt(2))) + pi)
            + log(sqrt(1 + sqrt(2)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi + pi) + log(-sqrt(2)/2 + sqrt(-S.Half + sqrt(2)))), S.Integers),
        ImageSet(Lambda(n, I*(2*n*pi - pi + atan(sqrt(2)*sqrt(S.Half + sqrt(2))))
            + log(sqrt(1 + sqrt(2)))), S.Integers)))
    f1 = (sinh(x)).rewrite(exp)
    f2 = (tanh(x)).rewrite(exp)
    assert dumeq(solveset(f1 + f2 - 1, x), Union(
        Complement(ImageSet(
            Lambda(n, I*(2*n*pi + pi) + log(-sqrt(2)/2 + sqrt(-S.Half + sqrt(2)))), S.Integers),
            ImageSet(Lambda(n, I*(2*n*pi + pi)/2), S.Integers)),
        Complement(ImageSet(Lambda(n, I*(2*n*pi - pi + atan(sqrt(2)*sqrt(S.Half + sqrt(2))))
                + log(sqrt(1 + sqrt(2)))), S.Integers),
            ImageSet(Lambda(n, I*(2*n*pi + pi)/2), S.Integers)),
        Complement(ImageSet(Lambda(n, I*(2*n*pi - atan(sqrt(2)*sqrt(S.Half + sqrt(2))) + pi)
                + log(sqrt(1 + sqrt(2)))), S.Integers),
            ImageSet(Lambda(n, I*(2*n*pi + pi)/2), S.Integers)),
        Complement(
            ImageSet(Lambda(n, 2*n*I*pi + log(sqrt(2)/2 + sqrt(-S.Half + sqrt(2)))), S.Integers),
            ImageSet(Lambda(n, I*(2*n*pi + pi)/2), S.Integers))))

