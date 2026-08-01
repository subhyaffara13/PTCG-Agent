
def generate_curves(n):
    points = [
        tuple(float(random.randint(0, 2048)) for coord in range(2))
        for point in range(1 + 3 * n)
    ]
    curves = []
    for i in range(n):
        curves.append(tuple(points[i * 3 : i * 3 + 4]))
    return curves

