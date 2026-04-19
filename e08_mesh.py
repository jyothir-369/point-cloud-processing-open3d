import open3d as o3d
import numpy as np


print("Testing mesh in Open3D...")

armadillo_mesh = o3d.data.ArmadilloMesh()
mesh = o3d.io.read_triangle_mesh(armadillo_mesh.path)
print(f' Armadillo info:')
print(mesh)
print(f'vertices:')

print(np.asarray(mesh.vertices))
print(f'Triangles:')
print(np.asarray(mesh.triangles))

#Surface normal estimation
mesh.compute_vertex_normals()

#Visualization
o3d.visualization.draw_geometries([mesh])

#Load another point cloud
knot_mesh = o3d.data.KnotMesh()
mesh = o3d.io.read_triangle_mesh(knot_mesh.path)

print(f' Knot info:')
print(mesh)
print(f'vertices:')

print(np.asarray(mesh.vertices))
print(f'Triangles:')
print(np.asarray(mesh.triangles))

print (f'Try to render Mesh with normal'
       f'(exists: {str(mesh.has_vertex_normals())})'
       f'(color: {str(mesh.has_vertex_colors())})'
)
# Surface normal estimation
mesh.compute_vertex_normals()

# Visualization
o3d.visualization.draw_geometries([mesh])

