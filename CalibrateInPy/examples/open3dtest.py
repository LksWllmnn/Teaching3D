#!/usr/bin/env python3.10

import open3d as o3d
import numpy as np
import cv2
from typing import List

def create_rotating_cube() -> o3d.geometry.LineSet:
    vertices: np.array = np.array([
        [0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [0.5, -0.5, 0.5], [0.5, -0.5, -0.5],
        [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, -0.5, -0.5]
    ])

    lines: List[List[int]] = [
        [0, 1], [1, 3], [3, 2], [2, 0],  # top face
        [4, 5], [5, 7], [7, 6], [6, 4],  # bottom face
        [0, 4], [1, 5], [2, 6], [3, 7]   # connecting lines
    ]

    colors: np.ndarray = np.array([[1, 0, 0] for _ in range(len(lines))])

    line_set: o3d.geometry.LineSet = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(vertices)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)

    return line_set

def main(): 
    cube: o3d.geometry.LineSet = create_rotating_cube()
    # Open3D Visualizer
    vis: o3d.visualization.Visualizer = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(cube)

    vis.run()
    vis.destroy_window()

if __name__ == "__main__":
    main()