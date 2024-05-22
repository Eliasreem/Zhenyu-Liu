import math
import yaml

# Load actions from the configuration file
with open('C:car_plan_0.yaml', 'r') as actions_file:
    actions_data = yaml.safe_load(actions_file)
    actions = actions_data['plan']  # Assuming the format is {'actions': [(s1, phi1), (s2, phi2), ...]}
# Initialize state variables
x, y, theta = 0.0, 0.0, 0.0  # Initial position and orientation

# Define car dynamics (adjust based on your model)
def update_state(u, dt):
    global x, y, theta
    s = u
    phi = u
    x += u * dt * math.cos(theta)
    y += u * dt * math.sin(theta)
    theta += phi * dt

# Integration parameters
dt = 0.1  # Time step (adjust as needed)

# Integrate dynamics
for u in actions:
    update_state(u, dt)

# Save the resulting plan
plan_data = {'states': [(x, y, theta)]}
with open('C:car_plan_0.yaml', 'w') as plan_file:
    yaml.dump(plan_data, plan_file)

print("Plan saved to cfg/car_plan_0.yaml")
