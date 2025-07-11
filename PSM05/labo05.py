import random
import turtle as t

STEP = 5
BASE_ANGLE = 25
CHAOS = 0.0
ITERATIONS = 6

stack = []

ALPHABET = {
    "F": lambda: advance(),
    "+": lambda: turn_left(),
    "-": lambda: turn_right(),
    "[": lambda: save_state(),
    "]": lambda: restore_state(),
}

RULES = {
    "F": "FF",
    "X": "F+[[X]-X]-F[-FX]+X",
}


def save_state():
    stack.append((t.position(), t.heading()))


def restore_state():
    position, heading = stack.pop()
    t.teleport(*position)
    t.setheading(heading)


def advance():
    delta = STEP * random.uniform(1 - CHAOS, 1 + CHAOS)
    t.forward(delta)


def turn(direction):
    delta = BASE_ANGLE * random.uniform(1 - CHAOS, 1 + CHAOS)
    t.setheading(t.heading() + direction * delta)


def turn_left():
    turn(1)


def turn_right():
    turn(-1)


def expand(axiom, iterations):
    for _ in range(iterations):
        axiom = "".join(RULES.get(ch, ch) for ch in axiom)
    return axiom


def draw():
    t.speed(0)
    t.hideturtle()
    t.tracer(0, 0)
    t.setheading(90)
    t.teleport(0, -t.window_height() / 2)

    for symbol in expand("X", ITERATIONS):
        action = ALPHABET.get(symbol)
        if action:
            action()

    t.update()
    t.done()


if __name__ == "__main__":
    draw()
