from amplpy import AMPL, Environment
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

class CirclePacking():

    def __init__(self, solver="octeract", initial_guess="random_gen"):
        self.solver = solver
        self.initial_guess = initial_guess
        self.ampl = AMPL(Environment())
        self.init_ampl()
        self.circle_centers = []


# ------------------------------------------------------------------------------------------

    def init_ampl(self):
        self.ampl.read("circle_packing.mod")
        self.ampl.read_data("circle_packing.dat")
        self.ampl.setOption('solver', self.solver)

        self.num_circles = int(self.ampl.getParameter('n').value())
        self.x_min = float(self.ampl.getParameter('Xmin').value())
        self.x_max = float(self.ampl.getParameter('Xmax').value())
        self.y_min = float(self.ampl.getParameter('Ymin').value())
        self.y_max = float(self.ampl.getParameter('Ymax').value())

        if self.initial_guess == "random":
            self.set_random_initial_values()
            self.plot_points_initial_values()
        elif self.initial_guess == "grid":
            self.set_grid_initial_values()
            self.plot_grid_initial_values()
        else:
            self.set_zero_initial_values()
            self.plot_points_initial_values()


    def set_zero_initial_values(self):
        self.circle_centers = []
        for _ in range(self.num_circles):
            self.circle_centers.append([0.0, 0.0])


    def set_grid_initial_values(self):
        # Calculate the smallest grid dimension G such that G*G >= n
        grid_dim = int(np.ceil(np.sqrt(self.num_circles)))

        num_linspace_points = grid_dim + 2
        self.xs = np.linspace(self.x_min, self.x_max, num_linspace_points)[1:-1]
        self.ys = np.linspace(self.y_min, self.y_max, num_linspace_points)[1:-1]
        grid_points = [[x, y] for x in self.xs for y in self.ys]

        self.circle_centers = random.sample(grid_points, self.num_circles)


    def set_random_initial_values(self):
        self.circle_centers = []
        for _ in range(self.num_circles):
            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(self.y_min, self.y_max)
            self.circle_centers.append([x, y])


    def optimize(self):
        self.ampl.solve()

        for i in range(1, circle_packing.num_circles + 1):
            x = self.ampl.var['x'][i].value()
            y = self.ampl.var['y'][i].value()
            self.circle_centers.append([x, y])

        self.radius = self.ampl.var['r'].value()

# ---------------------------------------------------------------------------

    def plot_grid_initial_values(self):
        fig, ax = plt.subplots()
        for x in self.xs:
            ax.axvline(x, color='gray', linestyle='--', linewidth=1)
        for y in self.ys:
            ax.axhline(y, color='gray', linestyle='--', linewidth=1)
        for center in self.circle_centers:
            ax.scatter(center[0], center[1], color='red', s=100, zorder=5)

        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.y_min, self.y_max)
        ax.set_aspect('equal', adjustable='box')
        ax.set_title("Initial Circle Positions on Grid")
        plt.show()

    def plot_points_initial_values(self):
        fig, ax = plt.subplots()

        for center in self.circle_centers:
            ax.scatter(center[0], center[1], color='red', s=100, zorder=5)

        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.y_min, self.y_max)
        ax.set_aspect('equal', adjustable='box')

        plt.show()

    def plot_results(self):
        fig, ax = plt.subplots()

        for center in self.circle_centers:
            x, y = center
            circle = patches.Circle((x, y), self.radius, linewidth=2, edgecolor='b', facecolor='none')
            ax.scatter(x, y, linewidths=2)
            ax.add_patch(circle)
            print(f"Circle center: {x}, {y}")
        print(f"Optimal Radius: {self.radius}")

        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.x_min, self.x_max)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()


solver_lut = {
    "ipopt": "/home/hojo/amplide/ampl.linux-intel64/ipopt",
    "baron": "/home/hojo/amplide/ampl.linux-intel64/baron",
    "lgo" : "/home/hojo/amplide/ampl.linux-intel64/lgo",
    "lindoglobal" : "/home/hojo/amplide/ampl.linux-intel64/lindoglobal",
    "octeract": "/home/hojo/amplide/ampl.linux-intel64/octeract",
    "couenne": "/home/hojo/amplide/ampl.linux-intel64/couenne",
    "knitro": "/home/hojo/amplide/ampl.linux-intel64/knitro"
}

if __name__ == "__main__":
    SEED = 1
    solver = solver_lut["knitro"]
    initial_guess = "grid" # [random, grid]

    random.seed(SEED)

    circle_packing = CirclePacking(solver=solver, initial_guess=initial_guess)
    circle_packing.optimize()
    circle_packing.plot_results()