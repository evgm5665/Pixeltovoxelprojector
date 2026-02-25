import os
import re
import math
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
import matplotlib.colors


def load_voxel_grid(filename):
    with open(filename, "rb") as f:
        N = np.frombuffer(f.read(4), dtype=np.int32)[0]
        voxel_size = np.frombuffer(f.read(4), dtype=np.float32)[0]
        count = N * N * N
        data = np.frombuffer(f.read(count * 4), dtype=np.float32)
        voxel_grid = data.reshape((N, N, N))
    return voxel_grid, voxel_size




# extract bright pixels
def extract_top_percentile_z_up(
    voxel_grid,
    voxel_size,
    grid_center,
    percentile=80.0,
):
    N = voxel_grid.shape[0]
    half_side = (N * voxel_size) * 0.5
    grid_min = grid_center - half_side

    flat_vals = voxel_grid.ravel()
    thresh = np.percentile(flat_vals, percentile)

    coords = np.argwhere(voxel_grid > thresh)

    if coords.size == 0:
        print("No voxels above threshold.")
        return None, None

    intensities = voxel_grid[coords[:, 0], coords[:, 1], coords[:, 2]]

    z_idx = coords[:, 0] + 0.5
    y_idx = coords[:, 1] + 0.5
    x_idx = coords[:, 2] + 0.5

    x_world = grid_min[0] + x_idx * voxel_size
    y_world = grid_min[1] + y_idx * voxel_size
    z_world = grid_min[2] + z_idx * voxel_size

    points = np.column_stack((x_world, y_world, z_world))

    return points.astype(np.float32), intensities.astype(np.float32)


def main():
    voxel_grid, vox_size = load_voxel_grid("output_voxel_grid.bin")

    print("Loaded voxel grid:", voxel_grid.shape)
    print("Voxel size:", vox_size)
    print("Max voxel value:", voxel_grid.max())
    print("Nonzero voxels:", np.count_nonzero(voxel_grid))

    grid_center = np.array([0, 0, 500], dtype=np.float32)

    percentile_to_show = 99.5

    points, intensities = extract_top_percentile_z_up(
        voxel_grid,
        voxel_size=vox_size,
        grid_center=grid_center,
        percentile=percentile_to_show,
    )

    if points is None:
        return

    # 
    # OPTIONAL ROTATION 
    # 
    R = rotation_matrix_xyz(0, 0, 0)
    points = points @ R.T

    print("Points count before downsample:", points.shape[0])
    print("Points min:", points.min(axis=0))
    print("Points max:", points.max(axis=0))

  
    # DOWN SAMPLE FOR RENDERING
    
    max_points = 200_000
    if points.shape[0] > max_points:
        idx = np.random.choice(points.shape[0], max_points, replace=False)
        points = points[idx]
        intensities = intensities[idx]
        print(f"Downsampled to {max_points} points")

    cloud = pv.PolyData(points)
    cloud["intensity"] = intensities

    print("Cloud bounds:", cloud.bounds)

    plotter = pv.Plotter()
    plotter.set_background("white")

    plotter.add_mesh(
        cloud,
        scalars="intensity",
        cmap="hot",
        style="points",
        point_size=6,
    )

    plotter.add_scalar_bar(title="Brightness")

    plotter.reset_camera()
    plotter.reset_camera_clipping_range()

    screenshot_folder = "screenshots"
    os.makedirs(screenshot_folder, exist_ok=True)
    next_idx = get_next_image_index(screenshot_folder)
    out_path = os.path.join(screenshot_folder, f"voxel_{next_idx:04d}.png")

    plotter.show(window_size=[1920, 1080], screenshot=out_path)

    print("Saved screenshot:", out_path)


if __name__ == "__main__":
    main()
