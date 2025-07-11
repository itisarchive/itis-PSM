import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.data_sets = []

    def add_to_plot(self, x, y, label):
        self.data_sets.append({'x': x, 'y': y, 'label': label})

    def plot(self, xlabel="X Position", ylabel="Y Position", title="Trajectory Plot", output_filename="trajectory.png", add_legend=True, figsize=(10, 6)):
        plt.figure(figsize=figsize)
        for data in self.data_sets:
            plt.plot(data['x'], data['y'], label=data['label'], linewidth=2)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        if add_legend:
            plt.legend()

        plt.grid(True)
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth=0.8, color='gray', alpha=0.7)
        plt.grid(which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.5)

        plt.savefig(output_filename, dpi=300)
        plt.show()
