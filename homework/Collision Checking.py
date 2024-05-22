import yaml
import fcl
from fcl.math import Vec3f, Transform3f
from fcl.collision_object import CollisionObject
from fcl.collision_geometry import Box
from fcl.bvh_mesh_loader import BVHModelFromFile  # 如果需要加载复杂的3D模型
from fcl.broadphase import BroadPhaseDynamicAABBTreeCollisionManager


def create_collision_object(pos, shape_type, size):
    if shape_type == 'box':
        geometry = Box(*size)
    else:
        raise ValueError(f"Unsupported shape type: {shape_type}")

    transform = Transform3f(Vec3f(0, 0, 0), Vec3f(*pos))  # 假设没有旋转
    return CollisionObject(geometry, transform)


def check_collisions(env_file, plan_file, output_file):
    with open(env_file, 'r') as file:
        env_data = yaml.safe_load(file)
    with open(plan_file, 'r') as file:
        plan_data = yaml.safe_load(file)

        # 创建环境障碍物碰撞对象
    obstacles = []
    for obstacle in env_data['obstacles']:
        obstacles.append(create_collision_object(obstacle['pos'], obstacle['type'], obstacle['size']))

        # 假设汽车是一个简单的长方体
    car_size = [plan_data['plan']['L'], plan_data['plan']['W'], plan_data['plan']['H']]
    car_collision_obj = create_collision_object([0, 0, 0], 'box', car_size)  # 初始位置

    # 创建碰撞管理器
    manager = BroadPhaseDynamicAABBTreeCollisionManager()
    manager.registerObjects(obstacles)  # 注册静态障碍物

    collisions = []

    # 检查每一步的碰撞情况
    for state, action in zip(plan_data['plan']['states'], plan_data['plan']['actions']):
        # 假设action是一个控制命令，这里简化为更新汽车位置（不考虑旋转）
        # 这里需要基于action和dt来计算新的位置，但为简单起见，我们直接使用给定的states
        car_pos = list(map(float, state))
        car_collision_obj.setTransform(Transform3f(Vec3f(0, 0, 0), Vec3f(*car_pos)))  # 更新汽车位置
        manager.update(car_collision_obj, True)  # 更新动态对象

        # 检查汽车是否与任何障碍物发生碰撞
        collision_result = any(manager.collide(car_collision_obj, other) for other in obstacles)
        collisions.append(collision_result)

        # 将结果写入输出文件
    with open(output_file, 'w') as file:
        yaml_data = {
            'collisions': collisions,
            'environment': env_data['environment'],
            'plan': {
                'type': plan_data['plan']['type'],
                'states': plan_data['plan']['states'],
                'actions': plan_data['plan']['actions']
            }
        }
        yaml.dump(yaml_data, file)

    # 示例用法


check_collisions('cfg/car_env_0.yaml', 'cfg/car_plan_0.yaml', 'collision_car_sol.yaml')