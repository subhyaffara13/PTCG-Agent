
def test_X5():
    # test case in Mathematica syntax:
    # In[21]:= (* => [a f'(a d) + g(b d) + integrate(h(c y), y = 0..d)]
    #       + [a^2 f''(a d) + b g'(b d) + h(c d)] (x - d) *)
    # In[22]:= D[f[a*x], x] + g[b*x] + Integrate[h[c*y], {y, 0, x}]
    # Out[22]= g[b x] + Integrate[h[c y], {y, 0, x}] + a f'[a x]
    # In[23]:= Series[%, {x, d, 1}]
    # Out[23]= (g[b d] + Integrate[h[c y], {y, 0, d}] + a f'[a d]) +
    #                                    2                               2
    #             (h[c d] + b g'[b d] + a  f''[a d]) (-d + x) + O[-d + x]
    h = Function('h')
    a, b, c, d = symbols('a b c d', real=True)
    # series() raises NotImplementedError:
    # The _eval_nseries method should be added to <class
    # 'sympy.core.function.Subs'> to give terms up to O(x**n) at x=0
    series(diff(f(a*x), x) + g(b*x) + integrate(h(c*y), (y, 0, x)),
           x, x0=d, n=2)

