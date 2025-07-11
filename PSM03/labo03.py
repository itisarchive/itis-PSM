from math import sin, cos, radians

from util.animate import AnimationPlotter
from util.plot import Plotter

energy_plotter = Plotter()
animation = AnimationPlotter()

gravity = -9.81
pendulum_length = 1
mass = 1
initial_angle = radians(45)
angle_shift = radians(90)
initial_speed = 0
time_step = 0.05

acceleration_function = lambda position, velocity: gravity / pendulum_length * sin(position)


def derivative(position, velocity, funcs):
    return velocity, funcs(position, velocity)


def euler_step(position, velocity, dt, funcs):
    dp, dv = derivative(position, velocity, funcs)
    return position + dp * dt, velocity + dv * dt


def midpoint_step(position, velocity, dt, funcs):
    dp1, dv1 = derivative(position, velocity, funcs)
    half_p = position + dp1 * dt * 0.5
    half_v = velocity + dv1 * dt * 0.5
    dp2, dv2 = derivative(half_p, half_v, funcs)
    return position + dp2 * dt, velocity + dv2 * dt


def runge_kutta_step(position, velocity, dt, funcs):
    dp1, dv1 = derivative(position, velocity, funcs)
    dp2, dv2 = derivative(position + dp1 * dt * 0.5, velocity + dv1 * dt * 0.5, funcs)
    dp3, dv3 = derivative(position + dp2 * dt * 0.5, velocity + dv2 * dt * 0.5, funcs)
    dp4, dv4 = derivative(position + dp3 * dt, velocity + dv3 * dt, funcs)
    np = position + (dp1 + 2 * dp2 + 2 * dp3 + dp4) / 6 * dt
    nv = velocity + (dv1 + 2 * dv2 + 2 * dv3 + dv4) / 6 * dt
    return np, nv


def compute_energies(position, velocity):
    x = pendulum_length * cos(position - angle_shift)
    y = pendulum_length * sin(position - angle_shift)
    h = y + pendulum_length
    ep = mass * abs(gravity) * h
    ek = mass * (velocity ** 2 * pendulum_length ** 2) / 2
    return ep, ek, ep + ek, x, y


def euler(position, velocity, dt):
    aser, wser, epser, ekser, etser, tser = [], [], [], [], [], []
    for i in range(10000):
        aser.append(position)
        wser.append(velocity)
        tser.append(i * dt)
        ep, ek, et, _, _ = compute_energies(position, velocity)
        epser.append(ep)
        ekser.append(ek)
        etser.append(et)
        position, velocity = euler_step(position, velocity, dt, acceleration_function)
    energy_plotter.add_to_plot(tser, epser, "Energia potencjalna (metoda Eulera)")
    energy_plotter.add_to_plot(tser, ekser, "Energia kinetyczna (metoda Eulera)")
    energy_plotter.add_to_plot(tser, etser, "Energia całkowita (metoda Eulera)")


def midpoint(position, velocity, dt):
    aser, wser, epser, ekser, etser, tser = [], [], [], [], [], []
    for i in range(1000):
        aser.append(position)
        wser.append(velocity)
        tser.append(i * dt)
        ep, ek, et, _, _ = compute_energies(position, velocity)
        epser.append(ep)
        ekser.append(ek)
        etser.append(et)
        position, velocity = midpoint_step(position, velocity, dt, acceleration_function)
    energy_plotter.add_to_plot(tser, epser, "Energia potencjalna (metoda Midpoint)")
    energy_plotter.add_to_plot(tser, ekser, "Energia kinetyczna (metoda Midpoint)")
    energy_plotter.add_to_plot(tser, etser, "Energia całkowita (metoda Midpoint)")


def runge_kutta(position, velocity, dt):
    aser, wser, epser, ekser, etser, tser, xser, yser = [], [], [], [], [], [], [], []
    for i in range(1000):
        aser.append(position)
        wser.append(velocity)
        tser.append(i * dt)
        ep, ek, et, x, y = compute_energies(position, velocity)
        xser.append(x)
        yser.append(y)
        epser.append(ep)
        ekser.append(ek)
        etser.append(et)
        position, velocity = runge_kutta_step(position, velocity, dt, acceleration_function)
    energy_plotter.add_to_plot(tser, epser, "Energia potencjalna (metoda Runge-Kutty)")
    energy_plotter.add_to_plot(tser, ekser, "Energia kinetyczna (metoda Runge-Kutty)")
    energy_plotter.add_to_plot(tser, etser, "Energia całkowita (metoda Runge-Kutty)")
    animation.add_to_animation(xser, yser, tser, "Ruch wahadła")


def main():
    euler(initial_angle, initial_speed, time_step)
    midpoint(initial_angle, initial_speed, time_step)
    runge_kutta(initial_angle, initial_speed, time_step)

    energy_plotter.plot(
        xlabel="Czas [s]",
        ylabel="Energia [J]",
        title="Energie potencjalna, kinetyczna i całkowita w funkcji czasu",
        output_filename="energy_plot.png",
        figsize=(20, 6)
    )

    animation.animate(
        xlabel="X Position",
        ylabel="Y Position",
        title="Ruch wahadła (metoda Runge-Kutty)",
        output_filename="pendulum_animation.gif",
        duration=10
    )


if __name__ == "__main__":
    main()
