# 2D LIDAR closest object follower

A simple script to receive 2D lidar measurements, and head the robot to the closest obstacle.

## Subscribed Topics
- scan: LaserScan


## Published Topics
- /hoverboard_velocity_controller/cmd_vel: Twist
- /arrow_marker: Marker (Points to the closest obstacle)
- /yaw: Float32 (Angle difference towards the closest obstacle)
- /index: Float32 (ID of the closest 2D LIDAR measurement)


# Launch
```bash
roslaunch htb_follower follower.launch

```

![repo](https://user-images.githubusercontent.com/24465803/196247333-debfadae-1691-404d-ac95-e6843186811d.png)
