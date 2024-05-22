import pybullet as p
import pybullet_data

# 连接到 PyBullet GUI（图形界面）或 DIRECT（无图形界面）
physicsClient = p.connect(p.GUI)  # 或者使用 p.DIRECT 来进入无图形界面模式
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # 设置 URDF 文件的搜索路径

# 设置重力
p.setGravity(0, 0, -10)

# 加载地面平面模型
planeId = p.loadURDF("plane.urdf")

# 设置机器人模型的初始位置和姿态
cubeStartPos = [0, 0, 1]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])

# 加载机器人模型（例如 r2d2.urdf）
boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)

# 开始模拟
p.stepSimulation()

# 获取机器人模型的位置和姿态
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)

# 打印机器人模型的位置和姿态
print(f"机器人模型位置：{cubePos}, 姿态：{cubeOrn}")

# 断开连接
p.disconnect()