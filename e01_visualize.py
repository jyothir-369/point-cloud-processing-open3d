import open3d as o3d
import argparse

'''
visualize point cloud data using the Open3D library in Python. 
The script loads a point cloud file and displays it using Open3D's 
interactive visualization tools.

To run the code: put your point cloud data inside the data/
then run: python visualize.py --input data/sample.ply
'''
def main():
    parser = argparse.ArgumentParser(description="Point Cloud Visualization with Open3D")
    parser.add_argument('--input', type=str, required=True, help='Path to the point cloud file')
    args = parser.parse_args()

    # Load the point cloud
    pcd = o3d.io.read_point_cloud(args.input)
    if pcd.is_empty():
        print(f"Failed to load point cloud: {args.input}")
        return

    print(f"Successfully loaded point cloud: {args.input}")
    print(pcd)  # Print basic information about the point cloud

    # Visualize the point cloud
    o3d.visualization.draw_geometries(
        [pcd],
        window_name='Open3D Point Cloud Visualization',
        width=800,
        height=600,
        left=50,
        top=50,
        point_show_normal=False
    )

if __name__ == "__main__":
    main()
