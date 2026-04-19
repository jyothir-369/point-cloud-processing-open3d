import open3d as o3d
import numpy as np
import cv2

def main():
    # Initialize RealSense camera
    import pyrealsense2 as rs

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    # Create Open3D visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window('Real-Time Point Cloud')

    pcd = o3d.geometry.PointCloud()
    geom_added = False

    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Create Open3D images
            depth_o3d = o3d.geometry.Image(depth_image)
            color_o3d = o3d.geometry.Image(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))

            rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
                color_o3d, depth_o3d,
                depth_scale=1000.0,
                depth_trunc=3.0,
                convert_rgb_to_intensity=False)

            # Get intrinsics
            intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
            pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
                intrinsics.width, intrinsics.height,
                intrinsics.fx, intrinsics.fy,
                intrinsics.ppx, intrinsics.ppy)

            # Generate point cloud
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
                rgbd_image, pinhole_camera_intrinsic)

            # Flip it, otherwise the point cloud will be upside down
            pcd.transform([[1, 0, 0, 0],
                           [0, -1, 0, 0],
                           [0, 0, -1, 0],
                           [0, 0, 0, 1]])

            # Visualize point cloud
            if not geom_added:
                vis.add_geometry(pcd)
                geom_added = True
            else:
                vis.update_geometry(pcd)
            vis.poll_events()
            vis.update_renderer()

            # Display RGB video in OpenCV window
            cv2.imshow('RGB Video', color_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Stop streaming
        pipeline.stop()
        cv2.destroyAllWindows()
        vis.destroy_window()

if __name__ == "__main__":
    main()
