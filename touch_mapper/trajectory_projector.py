# trajectory_projector.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from omni_msgs.msg import OmniState, OmniButtonEvent
import numpy as np


class TrajectoryProjector(Node):
    def __init__(self):
        super().__init__('trajectory_projector')

        # 标定参数（一旦成功标定，就永久保留，直到新标定覆盖）
        self.z_start = 0.0      # 米
        self.z_end = 0.0
        self.delta_z = 0.0      # 若 abs(delta_z) >= 0.001，则视为“已标定”

        # 交互状态机（仅控制按钮逻辑，不影响输出）
        self.interactive_state = 0  # 0=空闲, 1=等起点, 2=等终点
        self.current_z_m = 0.0
        self.last_grey = 0
        self.last_white = 0

        self.create_subscription(OmniState, '/phantom/state', self.state_callback, 10)
        self.create_subscription(OmniButtonEvent, '/phantom/button', self.button_callback, 10)
        self.publisher_ = self.create_publisher(Float64, '/touch/progress', 10)

        self.get_logger().info("🔄 系统启动。若未标定，按 WHITE BUTTON 开始标定...")

    def button_callback(self, msg):
        grey_rising = (msg.grey_button == 1 and self.last_grey == 0)
        white_rising = (msg.white_button == 1 and self.last_white == 0)
        self.last_grey = msg.grey_button
        self.last_white = msg.white_button

        if self.interactive_state == 0:
            if white_rising:
                self.interactive_state = 1
                self.get_logger().warn("✅ 进入标定模式。移动到起始位置，按 GREY BUTTON 记录起点。")

        elif self.interactive_state == 1:
            if grey_rising:
                self.z_start = self.current_z_m
                self.interactive_state = 2
                self.get_logger().warn(f"📌 起点 Z = {self.current_z_m*1000:.1f} mm。移动到终点，按 GREY BUTTON 记录终点。")
            elif white_rising:
                self.interactive_state = 0
                self.get_logger().info("↩️ 标定取消。")

        elif self.interactive_state == 2:
            if grey_rising:
                self.z_end = self.current_z_m
                self.delta_z = self.z_end - self.z_start
                if abs(self.delta_z) < 0.001:
                    self.get_logger().error("❌ Z范围太小！请拉开距离后重试。")
                    self.interactive_state = 1
                else:
                    self.interactive_state = 0  # 标定完成，回到空闲
                    direction = "正向" if self.delta_z > 0 else "反向"
                    self.get_logger().info(
                        f"🎯 标定完成！{direction}映射："
                        f"{self.z_start*1000:.1f} → {self.z_end*1000:.1f} mm "
                        f"(Δ={abs(self.delta_z)*1000:.1f} mm)"
                    )
            elif white_rising:
                self.interactive_state = 0
                self.get_logger().info("↩️ 标定取消。")

    def state_callback(self, msg):
        self.current_z_m = float(msg.pose.position.z) / 1000.0

        # ✅ 关键改进：只要曾经成功标定（delta_z 有效），就一直输出！
        if abs(self.delta_z) >= 0.001:  # 已标定
            s = (self.current_z_m - self.z_start) / self.delta_z
            s_clipped = np.clip(s, 0.0, 1.0)
            self.publisher_.publish(Float64(data=float(s_clipped)))
        else:
            # 未标定：可选择不发布，或发布 NaN/0（这里选择静默）
            # 可选：每5秒提醒一次（避免刷屏）
            pass


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = TrajectoryProjector()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()