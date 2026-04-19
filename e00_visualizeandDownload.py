import open3d as o3d

if __name__ == "__main__":
    dataset = o3d.data.BunnyMesh()
    pcd = o3d.io.read_point_cloud(dataset.path)

    # o3d.io.write_point_cloud("data/BunnyMesh.ply", pcd)
    o3d.visualization.draw(pcd)