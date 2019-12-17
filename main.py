from Curve import Curve
from Polynomial import Polynomial
from Point import Point
from sys import argv


def main():
    polynomials = {
        163: 'x^163+x^7+x^6+x^3+1',
        233: 'x^233+x^74+1',
        283: 'x^283+x^12+x^7+x^5+1',
        409: 'x^409+x^87+1',
        571: 'x^571+x^10+x^5+x^2+1',
        2: 'x^2+x+1',
        3: 'x^3+x+1',
        4: 'x^4+x+1',
        5: 'x^5+x^2+1',
        6: 'x^6+x+1',
        7: 'x^7+x^3+1',
        8: 'x^8+x^4+x^3+x^2+1',
        9: 'x^9+x^4+1',
        10: 'x^10+x^3+1',
        11: 'x^11+x^2+1',
        12: 'x^12+x^6+x^4+x+1',
        13: 'x^13+x^4+x^3+x+1',
        14: 'x^14+x^10+x^6+x+1',
        15: 'x^15+x+1',
        16: 'x^16+x^12+x^3+x+1',
        17: 'x^17+x^3+1',
        18: 'x^18+x^7+1',
        19: 'x^19+x^5+x^2+x+1',
        20: 'x^20+x^3+1',
    }

    file = argv[1]
    in_file = open(file, 'r')
    out_file = open('output.txt', 'w')

    curve_type = int(in_file.readline().strip())
    curve_p = None
    polynomial = None
    c = None
    if curve_type == 0:
        curve_p = create_polynomial(in_file.readline().strip())
        [a, b] = map(create_polynomial, in_file.readline().strip().split(" "))
    else:
        curve_polynomial_degree = create_polynomial(in_file.readline())
        curve_polynomial = polynomials.get(curve_polynomial_degree)
        [max_degree, curve_polynomial_coefficients] = parse_polynomial(curve_polynomial)
        polynomial_int = create_int_from_polynomial(curve_polynomial_coefficients)
        polynomial = Polynomial(polynomial_int)
        [a, b, c] = map(Polynomial, map(create_polynomial, in_file.readline().strip().split(" ")))
    curve = Curve(curve_p, polynomial, a, b, c)
    in_file.readline()
    rule_str = in_file.readline().strip()
    while rule_str != "":
        result = compute_rule(curve, rule_str, curve_type)
        out_file.write(str(result))
        out_file.write("\n")
        rule_str = in_file.readline().strip()

    in_file.close()
    out_file.close()


def create_int_from_polynomial(coefficients):
    bin_str = "".join(coefficients)
    return int(bin_str, 2)


def parse_polynomial(polynomial_str):
    coefficients = []
    polynomial_parts = polynomial_str.split("+")
    part = polynomial_parts[0]
    if part == "1":
        return 0, [1]
    else:
        [x, max_degree] = polynomial_parts[0].split("^")
        for i in range(0, int(max_degree) + 1):
            coefficients.append("0")
        for part in polynomial_parts:
            if part == "1":
                coefficients[int(max_degree)] = "1"
            elif part == "x":
                coefficients[int(max_degree) - 1] = "1"
            else:
                [x, degree] = part.split("^")
                coefficients[int(max_degree) - int(degree)] = "1"
    return max_degree, coefficients


def create_polynomial(arg: str):
    if arg.startswith("0x"):
        return int(arg, 16)
    if arg.startswith("0b"):
        return int(arg, 2)
    return int(arg, 10)


def compute_rule(curve, rule_str, curve_type):
    [operation, arg1, arg2] = rule_str.split(" ")
    if operation == "+":
        x, y = str(arg1).split(",")
        x = create_polynomial(x)
        y = create_polynomial(y)
        point1 = Point(x, y)
        x, y = str(arg2).split(",")
        x = create_polynomial(x)
        y = create_polynomial(y)
        point2 = Point(x, y)
        if curve_type == 1:
            point1 = Point(Polynomial(point1.x), Polynomial(point1.y))
            point2 = Point(Polynomial(point2.x), Polynomial(point2.y))
        return sum_points(curve, point1, point2, curve_type)
    if operation == "*":
        x, y = str(arg1).split(",")
        x = create_polynomial(x)
        y = create_polynomial(y)
        if curve_type == 1:
            point1 = Point(Polynomial(x), Polynomial(y))
        else:
            point1 = Point(x, y)
        coefficient = create_polynomial(arg2)
        return mul_points(curve, point1, coefficient, curve_type)


def sum_points(curve, point1, point2, curve_type):
    if curve_type == 0:
       return sum_z_points(curve, point1, point2)
    else:
        return sum_gf_points(curve, point1, point2)


def inverse(num, modulus):
    s, old_s = 0, 1
    r, old_r = modulus, num

    while r != 0:
        quotient = old_r // r

        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    gcd, x = old_r, old_s

    return x % modulus


def sum_z_points(curve, point1, point2):
    if point1.x != point2.x:
        k = ((point2.y - point1.y) * inverse(point2.x - point1.x, curve.p)) % curve.p
        x3 = (k*k - point1.x - point2.x) % curve.p
        y3 = (point1.y + k * (x3 - point1.x)) % curve.p
        return Point(x3, -y3 % curve.p)
    if point1.x == point2.x:
        if point1.y % curve.p == -point2.y % curve.p:
            return Point("O", "O")
        if point1.y == point2.y and point1.y == 0:
            return Point("O", "O")
        if point1.y == point2.y and point1.y != 0:
            k = ((3 * point1.x * point1.x + curve.a) * inverse(2 * point1.y, curve.p)) % curve.p
            x3 = (k * k - point1.x - point2.x) % curve.p
            y3 = (point1.y + k * (x3 - point1.x)) % curve.p
            return Point(x3, -y3 % curve.p )


def sum_gf_points(curve, point1, point2):
    if point1.x != point2.x:
        k = ((point2.y + point1.y) * (point2.x + point1.x).inverse(curve.polynomial)) % curve.polynomial
        x3 = (k * k + curve.a * k + curve.b - point1.x - point2.x) % curve.polynomial
        y3 = (point1.y + k * (x3 - point1.x)) % curve.polynomial
        return Point(x3, curve.a * x3 + y3)
    if point1.x == point2.x:
        if point2.y == curve.a * point1.x + point1.y % curve.polynomial:
            return Point("O", "O")
        else:
            k = ((point1.x * point1.x + curve.a * point1.y) * (curve.a * point1.x).inverse(curve.polynomial)) % curve.polynomial
            x3 = (k * k + curve.a * k + curve.b - point1.x - point2.x) % curve.polynomial
            y3 = (point1.y + k * (x3 - point1.x)) % curve.polynomial
            return Point(x3, curve.a * x3 + y3)


def mul_points(curve, point1, point2, curve_type):
    result = point1
    for i in range(0, point2 - 1):
        result = sum_points(curve, point1, result, curve_type)
    return result


if __name__ == '__main__':
    main()
