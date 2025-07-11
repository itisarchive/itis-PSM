import math
import sys

from util.plot import Plotter

term_cache = {}


def custom_sin(x, terms):
    term = x
    result = term
    for i in range(1, terms):
        if (i + 1) not in term_cache:
            term_cache[i + 1] = term * (-x * x) / ((2 * i) * (2 * i + 1))
        term = term_cache[i + 1]
        result += term
    return result


def move_to_correct_quadrant(x):
    while x < 0:
        x += 2 * math.pi
    x = x % (2 * math.pi)
    if 0 <= x <= math.pi / 2:
        return x, 1
    elif math.pi / 2 < x <= math.pi:
        return math.pi - x, 1
    elif math.pi < x <= 3 * math.pi / 2:
        return x - math.pi, -1
    else:
        return 2 * math.pi - x, -1


def degrees_to_radians(deg):
    return deg * (math.pi / 180)


def parse_input(args):
    if len(args) != 3:
        raise ValueError("Usage: python script.py <number> <unit>")
    val = float(eval(args[1]))
    unt = args[2]
    if unt not in ["rad", "deg"]:
        raise ValueError("The second argument must be either 'rad' or 'deg'.")
    return val, unt


def print_values(terms, approximations, exact, errors):
    cols = [
        ("n", 5, "right"),
        ("Result", 18, "right"),
        ("math.sin", 18, "right"),
        ("Error", 25, "right")
    ]

    def pad(t, w, a):
        s = str(t)
        if len(s) >= w:
            return s
        if a == "right":
            return s.rjust(w)
        return s.ljust(w)

    def sep():
        return "+" + "+".join("-" * c[1] for c in cols) + "+"

    print(sep())
    row = "|"
    for c in cols:
        row += pad(c[0], c[1], "right") + "|"
    print(row)
    print(sep())
    for i, r, m, e in zip(terms, approximations, exact, errors):
        row = "|"
        row += pad(i, cols[0][1], cols[0][2]) + "|"
        row += pad(f"{r:.13f}", cols[1][1], cols[1][2]) + "|"
        row += pad(f"{m:.13f}", cols[2][1], cols[2][2]) + "|"
        row += pad(f"{e:.22f}", cols[3][1], cols[3][2]) + "|"
        print(row)
        print(sep())


def main():
    v, u = parse_input(sys.argv)
    if u == "deg":
        angle = degrees_to_radians(v)
    else:
        angle = v
    corrected_angle, sign = move_to_correct_quadrant(angle)
    exact = math.sin(angle)
    terms, approximations, exacts, errors = [], [], [], []

    for i in range(1, 11):
        val = sign * custom_sin(corrected_angle, i)
        diff = abs(val - exact)
        terms.append(str(i))
        approximations.append(val)
        exacts.append(exact)
        errors.append(diff)

    print_values(terms, approximations, exacts, errors)
    plotter = Plotter()
    plotter.add_to_plot(range(1, 11), approximations, "Aproksymacja sin(x)")
    plotter.add_to_plot(range(1, 11), exacts, "Dokładne sin(x)")
    plotter.add_to_plot(range(1, 11), errors, "Błąd aproksymacji")
    plotter.plot(
        xlabel="Liczba wyrazów w serii",
        ylabel="Wartość / Błąd",
        title="Porównanie szeregu sin(x) z math.sin",
        output_filename="sin_series_plot.png"
    )


if __name__ == "__main__":
    main()
