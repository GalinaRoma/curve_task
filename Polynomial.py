class Polynomial:
    def __init__(self, bits: int):
        self.bits = bits

    def __add__(self, b):
        return Polynomial(self.bits ^ b.bits)

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other)

        return self.bits == other.bits

    def __len__(self):
        return self.bits.bit_length()

    def __lshift__(self, other):
        return Polynomial(self.bits << other)

    def __mod__(self, b):
        a = self.clone()

        while len(a) >= len(b):
            a += b << (len(a) - len(b))

        return a

    def __mul__(self, b):
        addend, s = self.clone(), Polynomial(0)

        for c in b.as_string:
            if c == '1':
                s += addend

            addend <<= 1

        return s

    def __str__(self):
        return bin(self.bits)

    def __sub__(self, b):
        return self + b

    @property
    def as_string(self):
        return bin(self.bits)[:1:-1]

    def clone(self):
        return Polynomial(self.bits)

    def _polydiv(self, divisor):
        quotient = Polynomial(0)
        remainder = self.clone()
        while len(remainder) >= len(divisor):
            product = Polynomial(1 << (len(remainder) - len(divisor)))
            quotient += product
            remainder += product * divisor

        return quotient

    def invert(self, p):
        old_t, t = Polynomial(0), Polynomial(1)
        old_r, r = p, self.clone()
        while r != Polynomial(0):
            quotient = old_r._polydiv(r)
            old_r, r = r, old_r + quotient * r
            old_t, t = t, old_t + quotient * t

        assert old_r.bits == 1  # old_r is the gcd
        return old_t % p
