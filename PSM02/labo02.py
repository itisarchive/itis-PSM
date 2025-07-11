from util.plot import Plotter

mass = 1.0
drag_coefficient = 0.5
gravity = [0.0, -10.0]
initial_position = [0.0, 0.0]
initial_velocity = [10.0, 10.0]


def acceleration_func(velocity):
    drag = [
        -drag_coefficient * v * abs(v)
        for v in velocity
    ]
    total_force = [
        mass * gravity[i] + drag[i]
        for i in range(len(velocity))
    ]
    return [
        total_force[i] / mass
        for i in range(len(velocity))
    ]


def interpolate_ground_crossing(prev_pos, curr_pos):
    y_prev = prev_pos[1]
    y_curr = curr_pos[1]
    t = y_prev / (y_prev - y_curr)
    return [
        prev_pos[i] + t * (curr_pos[i] - prev_pos[i])
        for i in range(len(prev_pos))
    ]


def euler_step(position, velocity, dt):
    a = acceleration_func(velocity)
    for i in range(len(position)):
        position[i] += velocity[i] * dt
        velocity[i] += a[i] * dt


def midpoint_step(position, velocity, dt):
    a1 = acceleration_func(velocity)
    half_pos = position[:]
    half_vel = velocity[:]
    for i in range(len(position)):
        half_pos[i] += velocity[i] * dt * 0.5
        half_vel[i] += a1[i] * dt * 0.5
    a2 = acceleration_func(half_vel)
    for i in range(len(position)):
        position[i] += half_vel[i] * dt
        velocity[i] += a2[i] * dt


def simulate_euler(dt):
    pos = initial_position[:]
    vel = initial_velocity[:]
    trajectory = [(pos[0], pos[1])]
    while pos[1] >= 0:
        previous = pos[:]
        euler_step(pos, vel, dt)
        if pos[1] < 0:
            pos = interpolate_ground_crossing(previous, pos)
        trajectory.append((pos[0], pos[1]))
        if pos[1] <= 0:
            break
    return trajectory


def simulate_midpoint(dt):
    pos = initial_position[:]
    vel = initial_velocity[:]
    trajectory = [(pos[0], pos[1])]
    while pos[1] >= 0:
        previous = pos[:]
        midpoint_step(pos, vel, dt)
        if pos[1] < 0:
            pos = interpolate_ground_crossing(previous, pos)
        trajectory.append((pos[0], pos[1]))
        if pos[1] <= 0:
            break
    return trajectory


def main():
    plotter = Plotter()

    traj_euler_1 = simulate_euler(0.1)
    x_euler_1 = [p[0] for p in traj_euler_1]
    y_euler_1 = [p[1] for p in traj_euler_1]
    plotter.add_to_plot(x_euler_1, y_euler_1, "Euler dt=0.1")

    traj_euler_2 = simulate_euler(0.01)
    x_euler_2 = [p[0] for p in traj_euler_2]
    y_euler_2 = [p[1] for p in traj_euler_2]
    plotter.add_to_plot(x_euler_2, y_euler_2, "Euler dt=0.01")

    traj_midpoint = simulate_midpoint(0.1)
    x_mid = [p[0] for p in traj_midpoint]
    y_mid = [p[1] for p in traj_midpoint]
    plotter.add_to_plot(x_mid, y_mid, "Midpoint dt=0.1")

    plotter.plot(
        xlabel="X",
        ylabel="Y",
        title="Trajektoria ruchu punktu z oporem i grawitacją",
        output_filename="trajectory.png"
    )


if __name__ == "__main__":
    main()
