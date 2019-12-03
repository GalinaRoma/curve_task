def main():
    in_file = open('input.txt', 'r')
    out_file = open('output.txt', 'w')

    curve_type = in_file.readline()
    if curve_type == 0:
        curve_p = in_file.readline()
        [a, b] = in_file.readline().split(" ")
    else:
        polynomial_str = in_file.readline()
        (curve_m, curve_polynomial) = parse_polynomial(polynomial_str)
        [a, b, c] = in_file.readline().split(" ")
    in_file.readline()
    rule_str = in_file.readline()
    while rule_str != "":
        rule = parse_rule(rule_str)
        result = compute_rule(rule)
        out_file.write(result)
        out_file.write("\n")

    in_file.close()
    out_file.close()


def parse_polynomial(polynomial_str):
    coefficients = []
    polynomial_parts = polynomial_str.split("+")
    part = polynomial_parts[0]
    if part == "1":
        return 0, [1]
    else:
        [x, max_degree] = polynomial_parts[0].split("^")
        for i in range(0, max_degree + 1, 1):
            coefficients[i] = 0
        for part in polynomial_parts:
            if part == "1":
                coefficients[0] = 1
            else:
                x, degree = part.split("^")
                coefficients[degree] = 1
    return max_degree, coefficients

def parse_rule():
    pass

def compute_rule():
    pass

if __name__ == '__main__':
    main()
