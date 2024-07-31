import math
import numpy as np
import pandas as pd
from scipy.linalg import eigh
import matplotlib.pyplot as plt
from depth.multivariate import *
import matplotlib.colors as mcolors
from numpy.random import RandomState
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# to split dataset into parts based on tolerance value
def split_dataframe_by_tolerance(df, column_name, tolerance, min_points=4):
    # Sort the dataframe based on the column
    df_sorted = df.sort_values(by=column_name).reset_index(drop=True)
    bins = []
    current_bin = []
    start_value = df_sorted[column_name].iloc[0]

    for idx, row in df_sorted.iterrows():
        if abs(row[column_name] - start_value) <= tolerance:
            current_bin.append(row)
        else:
            if len(current_bin) < min_points:
                # If the current bin has less than min_points, merge it with the previous bin
                if bins:
                    bins[-1] = pd.concat([bins[-1], pd.DataFrame(current_bin)])
                else:
                    bins.append(pd.DataFrame(current_bin))
            else:
                bins.append(pd.DataFrame(current_bin))
            current_bin = [row]
            start_value = row[column_name]

    if current_bin:
        if len(current_bin) < min_points and bins:
            bins[-1] = pd.concat([bins[-1], pd.DataFrame(current_bin)])
        else:
            bins.append(pd.DataFrame(current_bin))

    return bins


# Function to calculate the distance of a point from the camera perspective
def distance_from_camera(p, camera_position):
    return np.linalg.norm(p - camera_position)


# Function to plot a convex hull given an np array of points
#     view is the position of the viewport "camera" in a 3D plot
#     for more information refer to https://matplotlib.org/stable/api/toolkits/mplot3d/view_angles.html
def plot_convex_hull(ax, points, all, view=[30, 45, 15]):
    points = points.to_numpy()[:, :3]
    # Compute the convex hull and use delaunay triangulation to see if points are inside or outside hull
    hull = ConvexHull(points)

    # Camera position
    #   This value is just set to represent the camera position that is the default for 3D plots
    #   it would need to be changed manually if you alter the plot rendering angle.
    camera_position = np.array([1, 0, 1])

    distances = np.array(
        [distance_from_camera(point, camera_position) for point in points]
    )
    min_distance = distances.min()
    max_distance = distances.max()

    # Plot construction
    ax.view_init(elev=view[0], azim=view[1], roll=view[2])

    # Plotting the convex hull with color based on distance from camera point
    for simplex in hull.simplices:
        s = np.append(simplex, simplex[0])
        poly = Poly3DCollection([points[s]])

        # Calculate centroid of the facet
        centroid = np.mean(points[simplex], axis=0)

        # Calculate the distance of the centroid from the camera
        distance = distance_from_camera(centroid, camera_position)
        color_intensity = (distance - min_distance) / (max_distance - min_distance)

        # Map color_intensity to hue in HSV space, then convert to RGB
        hue = 1 - color_intensity  # Hue goes from 0 to 1
        saturation = 0.5  # Pastel colors have low saturation
        value = 1  # High value for light colors
        rgb_color = mcolors.hsv_to_rgb((hue, saturation, value))

        # Set color based on distance for pastel colors
        poly.set_facecolor((*rgb_color, 0.8))

        ax.add_collection3d(poly)

    # Plotting the points that are not inside the convex hull
    for point in all.to_numpy()[:, :3]:
        ax.scatter(
            point[0],
            point[1],
            point[2],
            color="cornflowerblue",
            marker=".",
            sizes=[0.075],
            alpha=0.2,
        )

    # Setting labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")


# Function to plot the progession of convex hull according to data depth
# given a dataset of points and their depths
def convex_hull_progression(
    df, tolerance, rows=2, fig_size=(12, 8), view=[30, 120, 60]
):
    # split dataset into n parts
    # parts = split_dataset(df, 'depth', n)[::-1]
    parts = split_dataframe_by_tolerance(df, "depth", tolerance)[::-1]

    # find number of columns
    index, l = 0, len(parts)
    columns = math.ceil(l / rows)

    # to store points for each convex hull
    current_points = pd.DataFrame([])

    if l <= 3:
        # creating figure according to given specifications
        fig, axs = plt.subplots(
            1, l, figsize=fig_size, subplot_kw=dict(projection="3d")
        )

        # add convex hull for each part to the figure
        while index < l:
            print(f"Plotting part {index+1}/{l}")
            current_points = pd.concat([parts[index], current_points])
            plot_convex_hull(axs[index], current_points, df, view)
            index += 1
    else:
        # creating figure according to given specifications
        fig, axs = plt.subplots(
            rows, columns, figsize=fig_size, subplot_kw=dict(projection="3d")
        )

        # add convex hull for each part to the figure
        for i in range(rows):
            for j in range(columns):
                if index < l:
                    print(f"Plotting part {index + 1}/{l}")
                    current_points = pd.concat([parts[index], current_points])
                    plot_convex_hull(axs[i, j], current_points, df, view)
                    index += 1
                else:
                    axs[i, j].axis("off")

    plt.show()
