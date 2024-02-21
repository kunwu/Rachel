import numpy as np
import matplotlib.pyplot as plt
from cube_slice import plot_cube

def run_not_web():
    point1 = np.array([80, 0, 100])
    point2 = np.array([100, 20, 100])
    point3 = np.array([100, 0, 80])
    plot_cube(point1, point2, point3)
    plt.show()

run_not_web()