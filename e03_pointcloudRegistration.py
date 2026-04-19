import open3d as o3d
import numpy as np
import copy
import argparse

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    # Apply the transformation to the source point cloud
    source_temp.transform(transformation)
    # Assign colors for visualization
    source_temp.paint_uniform_color([1, 0.706, 0])  # Yellow for source
    target_temp.paint_uniform_color([0, 0.651, 0.929])  # Blue for target
    # Visualize
    o3d.visualization.draw_geometries([source_temp, target_temp],
                                      window_name='Registration Result')

def preprocess_point_cloud(pcd, voxel_size):
    print(":: Downsampling with a voxel size of %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)
    # Estimate normals
    radius_normal = voxel_size * 2
    print(":: Estimating normals with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    return pcd_down

def compute_fpfh_feature(pcd, voxel_size):
    radius_feature = voxel_size * 5
    print(":: Computing FPFH features with search radius %.3f." % radius_feature)
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return fpfh

def prepare_dataset(voxel_size, source_path, target_path):
    print(":: Loading point clouds.")
    source = o3d.io.read_point_cloud(source_path)
    target = o3d.io.read_point_cloud(target_path)
    if source.is_empty() or target.is_empty():
        print("Error: Failed to load point clouds.")
        exit()

    source_down = preprocess_point_cloud(source, voxel_size)
    target_down = preprocess_point_cloud(target, voxel_size)

    source_fpfh = compute_fpfh_feature(source_down, voxel_size)
    target_fpfh = compute_fpfh_feature(target_down, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh

def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: Performing RANSAC registration.")
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, mutual_filter=True,
        max_correspondence_distance=distance_threshold,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        ransac_n=4,
        checkers=[
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)
        ],
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500)
    )
    return result

def execute_icp(source, target, initial_transformation, voxel_size):
    print(":: Performing ICP registration.")
    distance_threshold = voxel_size * 0.4
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, initial_transformation,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result

def main():
    parser = argparse.ArgumentParser(description="Point Cloud Registration with Open3D")
    parser.add_argument('--source', type=str, required=True, help='Path to the source point cloud file')
    parser.add_argument('--target', type=str, required=True, help='Path to the target point cloud file')
    args = parser.parse_args()

    voxel_size = 0.05  # Adjust the voxel size as needed

    # Load and preprocess point clouds
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(
        voxel_size, args.source, args.target)

    # Initial alignment using global registration
    result_global = execute_global_registration(source_down, target_down,
                                                source_fpfh, target_fpfh, voxel_size)
    print("Global registration transformation:")
    print(result_global.transformation)
    draw_registration_result(source, target, result_global.transformation)

    # Refine alignment using ICP
    result_icp = execute_icp(source, target, result_global.transformation, voxel_size)
    print("Refined registration transformation:")
    print(result_icp.transformation)
    draw_registration_result(source, target, result_icp.transformation)

if __name__ == "__main__":
    main()
