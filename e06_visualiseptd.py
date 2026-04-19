import numpy as np
import open3d as o3d

pcd = o3d.io.read_point_cloud('data/Armadillo.ply')
print(pcd)
print(np.asarray(pcd.points))
o3d.visualization.draw_geometries([pcd])
o3d.visualization.draw(pcd)