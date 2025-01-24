import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 읽기
# force_data = pd.read_csv('paper/forces_list_imp.csv', header=None).values  # time x 9
# end_effector_data = pd.read_csv('paper/ee_list_imp.csv', header=None).values  # time x 9
force_data = pd.read_csv('papercup/forces_list_imp_ver2.csv', header=None).values  # time x 9
end_effector_data = pd.read_csv('papercup/ee_list_imp_ver2.csv', header=None).values  # time x 9

# Force 데이터 처리
force_matrix = force_data  # (time_steps x 3)
finger1_force_xyz = force_matrix[5000:, 0:3]
finger2_force_xyz = force_matrix[5000:, 3:6]
finger3_force_xyz = force_matrix[5000:, 6:10]

# End-effector 데이터 처리
ee_matrix = end_effector_data  # (time_steps x 3)
finger1_ee_xyz = ee_matrix[5000:, 0:3]
finger2_ee_xyz = ee_matrix[5000:, 3:6]
finger3_ee_xyz = ee_matrix[5000:, 6:10]

# 플롯 설정
fig, axes = plt.subplots(3, 2, figsize=(15, 15))
fig.suptitle('Force and End-effector Data by Finger (Starting from Time Step 5000)', fontsize=16)

# Finger 1 데이터
axes[0, 0].plot(range(len(finger1_force_xyz)), finger1_force_xyz)
axes[0, 0].set_title('Finger 1 Force')
axes[0, 0].set_ylabel('Force (N)')
axes[0, 0].legend(['Fx', 'Fy', 'Fz'])

axes[0, 1].plot(range(len(finger1_ee_xyz)), finger1_ee_xyz)
axes[0, 1].set_title('Finger 1 End-effector')
axes[0, 1].set_ylabel('Position (m)')
axes[0, 1].legend(['Ex', 'Ey', 'Ez'])

# Finger 2 데이터
axes[1, 0].plot(range(len(finger2_force_xyz)), finger2_force_xyz)
axes[1, 0].set_title('Finger 2 Force')
axes[1, 0].set_ylabel('Force (N)')
axes[1, 0].legend(['Fx', 'Fy', 'Fz'])

axes[1, 1].plot(range(len(finger2_ee_xyz)), finger2_ee_xyz)
axes[1, 1].set_title('Finger 2 End-effector')
axes[1, 1].set_ylabel('Position (m)')
axes[1, 1].legend(['Ex', 'Ey', 'Ez'])

# Finger 3 데이터
axes[2, 0].plot(range(len(finger3_force_xyz)), finger3_force_xyz)
axes[2, 0].set_title('Finger 3 Force')
axes[2, 0].set_ylabel('Force (N)')
axes[2, 0].set_xlabel('Time Steps')
axes[2, 0].legend(['Fx', 'Fy', 'Fz'])

axes[2, 1].plot(range(len(finger3_ee_xyz)), finger3_ee_xyz)
axes[2, 1].set_title('Finger 3 End-effector')
axes[2, 1].set_ylabel('Position (m)')
axes[2, 1].set_xlabel('Time Steps')
axes[2, 1].legend(['Ex', 'Ey', 'Ez'])

# 레이아웃 조정
plt.tight_layout(rect=[0, 0, 1, 0.96])  # 전체 제목을 위한 여백
plt.show()
