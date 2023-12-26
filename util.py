from collections import defaultdict
from subprocess import Popen, PIPE


def canonical_decomposition(n: int) -> dict[int, int]:
    i = 2
    primes = defaultdict(int)
    while i * i <= n:
        while n % i == 0:
            primes[i] += 1
            n = n / i
        i = i + 1
    if n > 1:
        primes[i] += 1
    return primes


def gcd(a: int, b: int) -> tuple[int, int, int]:
    x1 = 1
    x2 = 0
    y1 = 0
    y2 = 1
    while b != 0:
        x_temp = x2
        y_temp = y2
        t = b
        x2 = x1 - x2 * (a // b)
        y2 = y1 - y2 * (a // b)
        x1 = x_temp
        y1 = y_temp
        b = a % b
        a = t
    return a, x1, y1


def encrypt(key: int, pt: int):
    return int(
        Popen(["./enc", str(key), str(pt)], stdout=PIPE).communicate()[0]
    )
