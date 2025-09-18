from amplpy import AMPL, Environment
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse

class CirclePacking():
    
    solver_lut = {
        "ipopt": "/home/hojo/amplide/ampl.linux-intel64/ipopt", 
        "baron": "/home/hojo/amplide/ampl.linux-intel64/baron",
        "lgo" : "/home/hojo/amplide/ampl.linux-intel64/lgo",
        "lindoglobal" : "/home/hojo/amplide/ampl.linux-intel64/lindoglobal", 
        "octeract": "/home/hojo/amplide/ampl.linux-intel64/octeract",
        "couenne": "/home/hojo/amplide/ampl.linux-intel64/couenne"
    }
    

    def __init__(self, n=2, solver="octeract"):
        self.x_min, self.x_max = 0.0, 10.0
        self.y_min, self.y_max = 0.0, 10.0

        self.circle_centers = []
        self.radius = 0.0

        self.num_circles = n
        if solver in CirclePacking.solver_lut:
            self.solver = CirclePacking.solver_lut[solver]
        else:
            print(f"Solver {solver} not recognized.")
            print(f"Choose between: ipopt, baron, lgo, lindoglobal, octeract, couenne")


    def optimize(self):
        with open("circle_packing.mod", "r") as file:
            ampl_code = file.read()

        ampl = AMPL(Environment())
        ampl.eval(ampl_code)
        ampl.param['n'].set(circle_packing.num_circles)
        ampl.param['Xmin'].set(self.x_min)
        ampl.param['Xmax'].set(self.x_max)
        ampl.param['Ymin'].set(self.y_min)
        ampl.param['Ymax'].set(self.y_max)

        ampl.setOption('solver', circle_packing.solver)
        ampl.solve()

        for i in range(1, circle_packing.num_circles+1):
            x = ampl.var['x'][i].value()
            y = ampl.var['y'][i].value()
            self.circle_centers.append([x, y])
        
        self.radius = ampl.var['r'].value()


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
    parser.add_argument("-n", "--circles", type=int, default=3, help="Number of circles")
    args = parser.parse_args()

    solver = args.solver
    n = args.circles

    if solver not in CirclePacking.solver_lut:
        print(f"Solver {solver} not recognized.")
        print(f"Choose between: ipopt, baron, lgo, lindoglobal, octeract, couenne")
        exit()

    circle_packing = CirclePacking(n=n, solver=solver)
    circle_packing.optimize()
    circle_packing.plot_results()