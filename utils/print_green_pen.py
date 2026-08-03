import sys

def printGreenPen(penName, funcs, file=sys.stdout, docstring=None):
    if docstring is not None:
        print('"""%s"""' % docstring)

    print(
        """from fontTools.pens.basePen import BasePen, OpenContourError
try:
	import cython
except (AttributeError, ImportError):
	# if cython not installed, use mock module with no-op decorators and types
	from fontTools.misc import cython
COMPILED = cython.compiled


__all__ = ["%s"]

class %s(BasePen):

	def __init__(self, glyphset=None):
		BasePen.__init__(self, glyphset)
"""
        % (penName, penName),
        file=file,
    )
    for name, f in funcs:
        print("		self.%s = 0" % name, file=file)
    print(
        """
	def _moveTo(self, p0):
		self._startPoint = p0

	def _closePath(self):
		p0 = self._getCurrentPoint()
		if p0 != self._startPoint:
			self._lineTo(self._startPoint)

	def _endPath(self):
		p0 = self._getCurrentPoint()
		if p0 != self._startPoint:
			raise OpenContourError(
							"Glyph statistics is not defined on open contours."
			)
""",
        end="",
        file=file,
    )

    for n in (1, 2, 3):
        subs = {P[i][j]: [X, Y][j][i] for i in range(n + 1) for j in range(2)}
        greens = [green(f, BezierCurve[n]) for name, f in funcs]
        greens = [sp.gcd_terms(f.collect(sum(P, ()))) for f in greens]  # Optimize
        greens = [f.subs(subs) for f in greens]  # Convert to p to x/y
        defs, exprs = sp.cse(
            greens,
            optimizations="basic",
            symbols=(sp.Symbol("r%d" % i) for i in count()),
        )

        print()
        for name, value in defs:
            print("	@cython.locals(%s=cython.double)" % name, file=file)
        if n == 1:
            print(
                """\
	@cython.locals(x0=cython.double, y0=cython.double)
	@cython.locals(x1=cython.double, y1=cython.double)
	def _lineTo(self, p1):
		x0,y0 = self._getCurrentPoint()
		x1,y1 = p1
""",
                file=file,
            )
        elif n == 2:
            print(
                """\
	@cython.locals(x0=cython.double, y0=cython.double)
	@cython.locals(x1=cython.double, y1=cython.double)
	@cython.locals(x2=cython.double, y2=cython.double)
	def _qCurveToOne(self, p1, p2):
		x0,y0 = self._getCurrentPoint()
		x1,y1 = p1
		x2,y2 = p2
""",
                file=file,
            )
        elif n == 3:
            print(
                """\
	@cython.locals(x0=cython.double, y0=cython.double)
	@cython.locals(x1=cython.double, y1=cython.double)
	@cython.locals(x2=cython.double, y2=cython.double)
	@cython.locals(x3=cython.double, y3=cython.double)
	def _curveToOne(self, p1, p2, p3):
		x0,y0 = self._getCurrentPoint()
		x1,y1 = p1
		x2,y2 = p2
		x3,y3 = p3
""",
                file=file,
            )
        for name, value in defs:
            print("		%s = %s" % (name, value), file=file)

        print(file=file)
        for name, value in zip([f[0] for f in funcs], exprs):
            print("		self.%s += %s" % (name, value), file=file)

    print(
        """
if __name__ == '__main__':
	from fontTools.misc.symfont import x, y, printGreenPen
	printGreenPen('%s', ["""
        % penName,
        file=file,
    )
    for name, f in funcs:
        print("		      ('%s', %s)," % (name, str(f)), file=file)
    print("		     ])", file=file)

