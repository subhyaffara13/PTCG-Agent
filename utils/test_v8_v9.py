
def test_V8_V9():
#Macsyma test case:
#(c27) /* This example involves several symbolic parameters
#   => 1/sqrt(b^2 - a^2) log([sqrt(b^2 - a^2) tan(x/2) + a + b]/
#                            [sqrt(b^2 - a^2) tan(x/2) - a - b])   (a^2 < b^2)
#      [Gradshteyn and Ryzhik 2.553(3)] */
#assume(b^2 > a^2)$
#(c28) integrate(1/(a + b*cos(x)), x);
#(c29) trigsimp(ratsimp(diff(%, x)));
#                        1
#(d29)             ------------
#                  b cos(x) + a
    raise NotImplementedError(
        "Integrate with assumption not supported")

