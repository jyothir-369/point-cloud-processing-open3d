import numpy as np
import open3d as o3d

# Load the point cloud data
file_path = "data/sample.xyz"
point_cloud = np.loadtxt(file_path, skiprows=1)

# Create a PointCloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:, :3])

# Check if colors are available and set them
if point_cloud.shape[1] >= 6:
    pcd.colors = o3d.utility.Vector3dVector(point_cloud[:, 3:6] / 255)

# Check if normals are available; if not, estimate them
if point_cloud.shape[1] >= 9:
    pcd.normals = o3d.utility.Vector3dVector(point_cloud[:, 6:9])
else:
    print("Normals not found in the file. Estimating normals.")
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# Compute the average distance between points to set the radii for BPA
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 1.5 * avg_dist  # You can adjust this multiplier based on your data

# Perform Ball-Pivoting Algorithm (BPA) for mesh reconstruction
radii = [radius, radius * 2]
bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd,
    o3d.utility.DoubleVector(radii)
)

# Optionally, simplify the mesh and clean up
bpa_mesh = bpa_mesh.simplify_quadric_decimation(target_number_of_triangles=100000)
bpa_mesh.remove_degenerate_triangles()
bpa_mesh.remove_duplicated_triangles()
bpa_mesh.remove_duplicated_vertices()
bpa_mesh.remove_non_manifold_edges()

# Visualize the reconstructed mesh
o3d.visualization.draw_geometries([bpa_mesh])
