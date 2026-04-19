import open3d as o3d
import argparse

def main():
    parser = argparse.ArgumentParser(description="Point Cloud Filtering with Open3D")
    parser.add_argument('--input', type=str, required=True, help='Path to the input point cloud file')
    args = parser.parse_args()

    # Load the point cloud
    pcd = o3d.io.read_point_cloud(args.input)
    if pcd.is_empty():
        print(f"Failed to load point cloud: {args.input}")
        return

    print("Original point cloud:")
    print(pcd)
    o3d.visualization.draw_geometries([pcd], window_name='Original Point Cloud')

    # Downsample the point cloud with a voxel size
    voxel_size = 0.02  # Adjust the voxel size as needed
    downpcd = pcd.voxel_down_sample(voxel_size=voxel_size)

    print("Downsampled point cloud:")
    print(downpcd)
    o3d.visualization.draw_geometries([downpcd], window_name='Downsampled Point Cloud')

    # Remove statistical outliers
    num_neighbors = 20
    std_ratio = 2.0
    cl, ind = downpcd.remove_statistical_outlier(nb_neighbors=num_neighbors,
                                                 std_ratio=std_ratio)
    inlier_cloud = downpcd.select_by_index(ind)
    outlier_cloud = downpcd.select_by_index(ind, invert=True)

    print("Point cloud after removing statistical outliers:")
    print(inlier_cloud)
    o3d.visualization.draw_geometries([inlier_cloud], window_name='Inlier Point Cloud')

    # Visualize inliers and outliers
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])  # Gray color for inliers
    outlier_cloud.paint_uniform_color([1, 0, 0])        # Red color for outliers

    print("Visualizing inliers (gray) and outliers (red):")
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      window_name='Inliers and Outliers')

if __name__ == "__main__":
    main()
