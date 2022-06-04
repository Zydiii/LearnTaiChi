import random

from taichi import approx

def test_minimization():
    from minimization import get_minimization, x, y, n

    for i in range(n):
        x[i] = random.random()
        y[i] = random.random()

    get_minimization()

    for i in range(n):
        assert x[i] == approx(y[i], rel=1e-4)

test_minimization()