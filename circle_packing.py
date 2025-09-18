from amplpy import AMPL, Environment
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CirclePacking():
    
    solver_lut = {
        "ipopt": "/home/hojo/amplide/ampl.linux-intel64/ipopt", 
        "baron": "/home/hojo/amplide/ampl.linux-intel64/baron",
        "lgo" : "/home/hojo/amplide/ampl.linux-intel64/lgo",
        "lindoglobal" : "/home/hojo/amplide/ampl.linux-intel64/lindoglobal", 
        "octeract": "/home/hojo/amplide/ampl.linux-intel64/octeract",
        "couenne": "/home/hojo/amplide/ampl.linux-intel64/couenne"
    }
    
    x_min, x_max = 0.0, 10.0
    y_min, y_max = 0.0, 10.0

    solver = solver_lut["octeract"]
    num_circles = 5
    circle_centers = []
    

    def optimize(self):

        ampl_code = """
            param n integer > 0;
            param Xmin;
            param Xmax;
            param Ymin;
            param Ymax;

            var x {1..n};
            var y {1..n};
            var r >= 0;

            maximize Radius: r;

            subject to InBoxX_lower {i in 1..n}:
                Xmin + r <= x[i];

            subject to InBoxX_upper {i in 1..n}:
                x[i] <= Xmax - r;

            subject to InBoxY_lower {i in 1..n}:
                Ymin + r <= y[i];

            subject to InBoxY_upper {i in 1..n}:
                y[i] <= Ymax - r;

            subject to NoOverlap {i in 1..n, j in 1..n: i < j}:
                (x[i] - x[j])^2 + (y[i] - y[j])^2 >= (2 * r)^2;
        """

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

    circle_packing = CirclePacking()
    circle_packing.optimize()
    circle_packing.plot_results()