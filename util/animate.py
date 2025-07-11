import matplotlib.animation as animation
import matplotlib.pyplot as plt


class AnimationPlotter:
    def __init__(self):
        self.data_sets = []

    def add_to_animation(self, x, y, t, label="Dataset"):
        if not (len(x) == len(y) == len(t)):
            raise ValueError("Listy x, y i t muszą mieć taką samą długość.")
        self.data_sets.append({'x': x, 'y': y, 't': t, 'label': label})

    def animate(self, xlabel="X Position", ylabel="Y Position", title="Animation",
                output_filename="animation.gif", duration=None):
        if not self.data_sets:
            print("Brak danych do animacji.")
            return

        nframes = len(self.data_sets[0]['x'])

        if duration is not None:
            interval = (duration / nframes) * 1000
        else:
            interval = 33

        all_x = [x for data in self.data_sets for x in data['x']]
        all_y = [y for data in self.data_sets for y in data['y']]
        margin = 0.1
        xmin, xmax = min(all_x), max(all_x)
        ymin, ymax = min(all_y), max(all_y)
        xrange = xmax - xmin
        yrange = ymax - ymin
        xmin -= margin * xrange
        xmax += margin * xrange
        ymin -= margin * yrange
        ymax += margin * yrange

        fig, ax = plt.subplots(figsize=(20, 6))
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True)

        lines = []
        markers = []
        for data in self.data_sets:
            line, = ax.plot([], [], label=data['label'], lw=2)
            marker, = ax.plot([], [], 'o')
            lines.append(line)
            markers.append(marker)

        ax.legend()

        def init():
            for line, marker in zip(lines, markers):
                line.set_data([], [])
                marker.set_data([], [])
            return lines + markers

        def update(frame):
            for idx, data in enumerate(self.data_sets):
                i = frame if frame < len(data['x']) else len(data['x']) - 1
                lines[idx].set_data(data['x'][:i + 1], data['y'][:i + 1])
                markers[idx].set_data([data['x'][i]], [data['y'][i]])
            return lines + markers

        ani = animation.FuncAnimation(fig, update, frames=nframes, init_func=init,
                                      blit=True, interval=interval)

        ani.save(output_filename, writer='pillow', dpi=200)
        plt.show()
