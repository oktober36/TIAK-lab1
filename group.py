import random
from collections import defaultdict
from enum import Enum
from typing import Callable

from util import canonical_decomposition, gcd


class ModType(Enum):
    num2 = "2"
    num4 = "4"
    p = "p"
    pk = "p^k"


class Group:
    def __init__(self, mod):
        decom = canonical_decomposition(mod)
        self._mod_type: ModType

        if mod == 2:
            self._mod_type = ModType.num2
        elif mod == 4:
            self._mod_type = ModType.num4
        elif sum(decom.values()) == 1:
            self._mod_type = ModType.p
        elif len(decom) == 1:
            self._mod_type = ModType.pk
        elif len(decom) == 2 and decom[2] == 1:
            raise NotImplementedError
        else:
            raise Exception("Module is not 2, 4, p^k, 2p^k")
        self._mod = mod
        self._mod_decom = decom

    def _parse_primitive_root(self, x: int) -> int:
        assert x < self._mod

        if self._mod_type in (ModType.num2, ModType.num4, ModType.p):
            return x * (self._mod % x != 0)

        else:
            ((p, k),) = self._mod_decom.items()

            if gcd(x, p) != 1:
                return 0

            for q_i in self._mod_decom:
                if pow(x, int((p - 1) / q_i), p) == 1:
                    return 0

            if k == 1:
                return x

            else:
                if pow(x, p - 1, p * p) != 1:
                    return x
                if pow(x + p, p - 1, p * p) != 1:
                    return x + p
                return 0

    def get_random_primitive_root(self):
        if 2 in self._mod_decom and self._mod != 2:
            raise NotImplementedError

        if sum(self._mod_decom.values()) == 1:
            return random.choice(range(2, self._mod - 1))

        while True:
            a = random.choice(range(2, self._mod - 1))

            if a_ := self._parse_primitive_root(a):
                return a_

    def pohlig_hellman(self, hash_func: Callable[[int | str, int | str], int]) -> (int, int):
        q_map = canonical_decomposition(self._mod - 1)
        r: defaultdict[int, dict] = defaultdict(dict)
        x: defaultdict[int, list] = defaultdict(list)

        root = self.get_random_primitive_root()
        for q_i in q_map:
            for j in range(0, q_i):
                r[q_i][hash_func(root, j * (self._mod - 1) // q_i)] = j
            x[q_i].append(r[q_i][hash_func("k", (self._mod - 1) // q_i)])

        array_for_crt = []
        for q_i in q_map:
            temp_x = 0
            for i in range(q_map[q_i]):
                temp_x += x[q_i][i] * (q_i**i) % (q_i ** q_map[q_i])
            array_for_crt.append([temp_x, (q_i ** q_map[q_i])])

        return root, crt(array_for_crt)


def crt(a) -> int:
    m = 1
    for i in a:
        m *= i[1]
    result = 0
    for i in a:
        _, _, m_inv = gcd(i[1], m // i[1])
        result = (result + i[0] * m // i[1] * m_inv) % m
    return result
