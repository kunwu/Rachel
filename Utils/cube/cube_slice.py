import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define cube vertices
vertices = np.array([[0, 0, 0],
                     [0, 0, 1],
                     [0, 1, 0],
                     [0, 1, 1],
                     [1, 0, 0],
                     [1, 0, 1],
                     [1, 1, 0],
                     [1, 1, 1]]) * 100

# Define cube edges
edges = [[0, 1], [0, 2], [0, 4],
         [1, 3], [1, 5],
         [2, 3], [2, 6],
         [3, 7],
         [4, 5], [4, 6],
         [5, 7],
         [6, 7]]

# Define three points on the plane (modify these points according to your desired plane)
point1 = np.array([80, 0, 100])
point2 = np.array([100, 20, 100])
point3 = np.array([100, 0, 80])
# 正六边形
# point1 = np.array([100, 50, 100])
# point2 = np.array([50, 100, 100])
# point3 = np.array([100, 0, 50])

# Calculate the normal vector to the plane
normal_vector = np.cross(point2 - point1, point3 - point1)

# Normalize the normal vector
normalized_normal_vector = normal_vector / np.linalg.norm(normal_vector)

# Extract the coefficients a, b, c from the normalized normal vector
a, b, c = normalized_normal_vector

# Calculate the d coefficient of the plane equation
d = -np.dot(normalized_normal_vector, point1)

# Define grid points on the plane with offset
xmin, xmax = -0.2, 1.2
ymin, ymax = -0.2, 1.2
n = 50  # Number of grid points
xx, yy = np.meshgrid(np.linspace(xmin, xmax, n), np.linspace(ymin, ymax, n))
zz = (-d - a * xx - b * yy) / c

# Calculate intersection points
intersections = []
for edge in edges:
    v1, v2 = vertices[edge[0]], vertices[edge[1]]
    if (a * v1[0] + b * v1[1] + c * v1[2] + d) * (a * v2[0] + b * v2[1] + c * v2[2] + d) < 0:
        t = (a * v1[0] + b * v1[1] + c * v1[2] + d) / ((a * v1[0] + b * v1[1] + c * v1[2] + d) - (a * v2[0] + b * v2[1] + c * v2[2] + d))
        intersection = v1 + t * (v2 - v1)
        intersections.append(intersection)

# Convert intersections list to NumPy array
intersections = np.array(intersections)

# Find the center point of the intersection plane
center_point = np.mean(intersections, axis=0)

# Compute the angles of each intersection point with respect to the center point
angles = np.arctan2(intersections[:, 1] - center_point[1], intersections[:, 0] - center_point[0])

# Sort the intersection points based on their angles
sorted_indices = np.argsort(angles)
sorted_intersections = intersections[sorted_indices]
intersections = sorted_intersections

# Calculate number of edges and vertices
num_edges = len(intersections)
num_vertices = len(set(tuple(point) for point in intersections))

print("Number of Edges:", num_edges)
print("Number of Vertices:", num_vertices)


# Create 3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Add text to the chart
ax.text(-50, 0, 120, f'Number of vertices: {num_vertices}', color='black')
ax.text(-50, 0, 110, f'Number of edges: {num_edges}', color='black')

# Plot cube
for edge in edges:
    ax.plot3D(*zip(vertices[edge[0]], vertices[edge[1]]), color='k')

# Generate a mesh grid
x_range = np.linspace(min(intersections[:, 0]), max(intersections[:, 0]), 10)
y_range = np.linspace(min(intersections[:, 1]), max(intersections[:, 1]), 10)
x_coords, y_coords = np.meshgrid(x_range, y_range)
z_coords = (-d - a * x_coords - b * y_coords) / c  # Use plane equation to calculate z coordinates

# Plot the plane as a surface
ax.plot_surface(x_coords, y_coords, z_coords, alpha=0.3)

# Plot cut face
face = Poly3DCollection([intersections], alpha=0.2, linewidths=1, edgecolors='k')
face.set_facecolor('lightblue')
ax.add_collection3d(face)

ax.text(point1[0], point1[1], point1[2], 'p1', color='red')
ax.text(point2[0], point2[1], point2[2], 'p2', color='green')
ax.text(point3[0], point3[1], point3[2], 'p3', color='blue')

# Set plot limits and labels
ax.set_xlim([0, 1 * 100])
ax.set_ylim([0, 1 * 100])
ax.set_zlim([0, 1 * 100])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Emphasize the origin point
ax.scatter3D(0, 0, 0, color='#991100', s=50)

# Add arrows to each axis
arrow_length = 18  # Decrease this to make the arrow head appear smaller
arrow_linewidth = 1.5  # Increase this to make the arrow head appear smaller
ax.quiver(0, 0, 0, arrow_length, 0, 0, color='#991100', linewidth=arrow_linewidth)
ax.quiver(0, 0, 0, 0, arrow_length, 0, color='#991100', linewidth=arrow_linewidth)
ax.quiver(0, 0, 0, 0, 0, arrow_length, color='#991100', linewidth=arrow_linewidth)
ax.text(18, 0, 0, 'X', color='#991100', fontweight='bold')
ax.text(0, 18, 0, 'Y', color='#991100', fontweight='bold')
ax.text(0, 0, 18, 'Z', color='#991100', fontweight='bold')

# Show the plot
plt.show()
