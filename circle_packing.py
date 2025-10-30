from amplpy import AMPL, Environment
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import numpy as np

class CirclePacking():

    solver_lut = {
        "ipopt": "/home/hojo/amplide/ampl.linux-intel64/ipopt",
        "baron": "/home/hojo/amplide/ampl.linux-intel64/baron",
        "lgo" : "/home/hojo/amplide/ampl.linux-intel64/lgo",
        "lindoglobal" : "/home/hojo/amplide/ampl.linux-intel64/lindoglobal",
        "octeract": "/home/hojo/amplide/ampl.linux-intel64/octeract",
        "couenne": "/home/hojo/amplide/ampl.linux-intel64/couenne",
        "knitro": "/home/hojo/amplide/ampl.linux-intel64/knitro"
    }


    def __init__(self, solver="octeract"):
        self.ampl = AMPL(Environment())
        if solver in CirclePacking.solver_lut:
            self.solver = CirclePacking.solver_lut[solver]
        else:
            raise ValueError(f"Solver {solver} not recognized.")
        self.init_ampl()
        self.circle_centers = []

    def init_ampl(self):
        self.ampl.read("circle_packing.mod")
        self.ampl.read_data("circle_packing.dat")
        self.ampl.setOption('solver', self.solver)

        self.num_circles = int(self.ampl.getParameter('n').value())
        self.x_min = float(self.ampl.getParameter('Xmin').value())
        self.x_max = float(self.ampl.getParameter('Xmax').value())
        self.y_min = float(self.ampl.getParameter('Ymin').value())
        self.y_max = float(self.ampl.getParameter('Ymax').value())


    def set_initial_values(self, num_points):
        grid_size = int(np.ceil(np.sqrt(num_points)))
        xs = np.linspace(self.x_min, self.x_max, grid_size)
        ys = np.linspace(self.y_min, self.y_max, grid_size)
        grid_points = [[x, y] for x in xs for y in ys]
        self.circle_centers = grid_points[:num_points]
        return self.circle_centers

    def get_results(self):
        for i in range(1, circle_packing.num_circles + 1):
            x = self.ampl.var['x'][i].value()
            y = self.ampl.var['y'][i].value()
            self.circle_centers.append([x, y])

        self.radius = self.ampl.var['r'].value()

    def optimize(self):
        self.ampl.solve()
        self.get_results()


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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--solver", type=str, default="octeract", help="Solver to use: ipopt, baron, lgo, lindoglobal, octeract, couenne")
    args = parser.parse_args()

    solver = args.solver

    if solver not in CirclePacking.solver_lut:
        print(f"Solver {solver} not recognized.")
        print(f"Choose between: ipopt, baron, lgo, lindoglobal, octeract, couenne")
        exit()

    circle_packing = CirclePacking(solver=solver)
    circle_packing.optimize()
    circle_packing.plot_results()