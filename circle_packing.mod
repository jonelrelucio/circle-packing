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