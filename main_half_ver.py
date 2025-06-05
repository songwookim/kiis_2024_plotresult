import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Butterworth Low-pass Filter 함수
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs  # Nyquist 주파수
    normal_cutoff = cutoff / nyquist  # 정규화된 컷오프 주파수
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data, axis=0)  # 필터 적용
    return y


# CSV 파일 읽기
# force_data = pd.read_csv('paper/forces_list_imp.csv', header=None).values  # time x 9
# end_effector_data = pd.read_csv('paper/ee_list_imp.csv', header=None).values  # time x 9
is_paper = 0
is_imp = 1

timestep_start = 5000
timestep_end = 7000
LINE_WIDTH = 4
HLINE_WIDTH = 1.5

if is_paper :
    obj = 'paper'
else :
    obj = 'papercup'
if is_imp :
    law = 'imp'
else : 
    law = 'pd'

path_forces = f'{obj}/forces_list_{law}_ver2.csv'
path_ee = f'{obj}/ee_list_{law}_ver2.csv'

force_data = pd.read_csv(path_forces, header=None).values  # time x 9
end_effector_data = pd.read_csv(path_ee, header=None).values  # time x 9

# # force_data와 end_effector_data 각각에 필터 적용
# 파라미터 설정
cutoff = 5.0  # 컷오프 주파수 (Hz)
if is_paper :
    fs = 1024  # 샘플링 주파수 (Hz)
else :
    fs = 512
order = 4  # 필터 차수
force_data = butter_lowpass_filter(force_data, cutoff, fs, order)
# end_effector_data = butter_lowpass_filter(end_effector_data, cutoff, fs, order)

# Force 데이터 처리
force_matrix = force_data  # (time_steps x 3)
finger1_force_xyz = force_matrix[timestep_start:timestep_end, 0:3]
finger2_force_xyz = force_matrix[timestep_start:timestep_end, 3:6]
finger3_force_xyz = force_matrix[timestep_start:timestep_end, 6:10]

# End-effector 데이터 처리
ee_matrix = end_effector_data  # (time_steps x 3)
finger1_ee_xyz = ee_matrix[timestep_start:timestep_end, 0:3]
finger2_ee_xyz = ee_matrix[timestep_start:timestep_end, 3:6]
finger3_ee_xyz = ee_matrix[timestep_start:timestep_end, 6:10]



ee_y_min = -0.085
ee_y_max = 0.085
font_size_title = 36
font_size_tick = 28
font_size_legend = 20

xticks = [0, 1000, 2000]
xtick_labels = ['0', '1', '2']
if is_paper :
    force_y_min = -0.5
    force_y_max = 1.2
    yticks_f = [-0.4, 0, 0.4, 0.8, 1.2]
    ytick_labels_f = [-0.4, 0, 0.4, 0.8, 1.2]

    yticks_e = [-0.08, -0.04, 0, 0.04, 0.08]
    ytick_labels_e = [-0.08, -0.04, 0, 0.04, 0.08]
else :
    force_y_min = -1.75
    force_y_max = 4.5
    yticks_f = [-1.75, 0, 1.75, 3, 4.5]
    ytick_labels_f = [-1.75, 0, 1.75, 3, 4.5]
    
    yticks_e = [-0.08, -0.04, 0, 0.04, 0.08]
    ytick_labels_e = [-0.08, -0.04, 0, 0.04, 0.08]

# 플롯 설정
fig, axes = plt.subplots(3, 2, figsize=(15, 15))
if is_imp:
    # fig.suptitle(f'Impedance control', fontsize=font_size_title)
    fig.suptitle(f'Experiment 1 : Grasping a Paper Cup with Minor Deformation', fontsize=24)
    fig.suptitle(f'Experiment 2 : Grasping a Paper Cynlinder with Minor Deformation', fontsize=24)
else :
    
    fig.suptitle('PD control', fontsize=font_size_title)

for i in range(3):  # finger index
    # Force 데이터 (red, green, blue)
    for j, (color, label) in enumerate(zip(['r', 'g', 'b'], ['Fx', 'Fy', 'Fz'])):
        fm = force_matrix[timestep_start:timestep_end, 0 + 3 * i:3 + 3 * i]
        axes[i, 0].plot(range(len(fm[:, j])), fm[:, j],
                        color=color, linewidth=LINE_WIDTH, label=label)
        
        axes[i, 0].set_xticks(xticks)
        axes[i, 0].set_xticklabels(xtick_labels, fontsize=font_size_tick)  # Tick 폰트 크기 및 굵기
        axes[i, 0].set_yticks(yticks_f)
        axes[i, 0].set_yticklabels(ytick_labels_f, fontsize=font_size_tick)
        axes[i, 0].set_ylabel('Force (N)', fontsize=font_size_tick)
        # 0 값 기준으로 검정 점선 추가
        axes[i, 0].axhline(0, color='k', linestyle='--', linewidth=HLINE_WIDTH, label='_nolegend_')

        # axes[i, 0].grid(True, axis='y')
        axes[i, 0].grid(True)
        axes[i, 0].set_ylim([force_y_min, force_y_max])

        axes[i, 0].legend(['Fx', 'Fy', 'Fz'], fontsize=font_size_legend, loc='upper right', frameon=True, facecolor='white')  # Legend 폰트 크기

    # End-effector 데이터 (cyan, magenta, yellow)
    for j, (color, label) in enumerate(zip(['c', 'm', 'y'], ['Ex', 'Ey', 'Ez'])):
        em = ee_matrix[timestep_start:timestep_end, 0 + 3 * i:3 + 3 * i]
        axes[i, 1].plot(range(len(em[:, j])), em[:, j],
                        color=color, linewidth=LINE_WIDTH, label=label)
        axes[i, 1].set_xticks(xticks)
        axes[i, 1].set_xticklabels(xtick_labels, fontsize=font_size_tick)  # Tick 폰트 크기 및 굵기
        axes[i, 1].set_yticks(yticks_e)
        axes[i, 1].set_yticklabels(ytick_labels_e, fontsize=font_size_tick)
        axes[i, 1].set_ylabel('Position [m]', fontsize=font_size_tick)
        # axes[i, 1].set_xlabel('Time (ms)')
        # 0 값 기준으로 검정 점선 추가
        axes[i, 1].axhline(0, color='k', linestyle='--', linewidth=HLINE_WIDTH ,label='_nolegend_')

        axes[i, 1].grid(True)
        axes[i, 1].set_ylim([ee_y_min, ee_y_max])
        
        axes[i, 1].legend(['Ex', 'Ey', 'Ez'], fontsize=font_size_legend, loc='upper right', frameon=True, facecolor='white')  # Legend 폰트 크기

        

    # for j, (color, label) in enumerate(zip(['cyan','magenta','yellow'], ['Ex','Ey','Ez'])):


# axes[0, 0].plot(range(len(finger1_force_xyz)), finger1_force_xyz, linewidth=LINE_WIDTH)
# axes[0, 0].set_title('Finger 1 Force')
# axes[0, 0].set_ylabel('Force (N)')
# axes[0, 0].legend(['Fx', 'Fy', 'Fz'])
# axes[0, 0].set_ylim([force_y_min, force_y_max])


# axes[0, 1].plot(range(len(finger1_ee_xyz)), finger1_ee_xyz, linewidth=LINE_WIDTH)
# axes[0, 1].set_title('Finger 1 End-effector')
# axes[0, 1].set_ylabel('Position (m)')
# axes[0, 1].legend(['Ex', 'Ey', 'Ez'])
# axes[0, 1].set_ylim([ee_y_min, ee_y_max])
# axes[0, 0].set_xticks([0, 1000, 2000])

# Finger 2 데이터
# axes[1, 0].plot(range(len(finger2_force_xyz)), finger2_force_xyz, linewidth=LINE_WIDTH)
# axes[1, 0].set_title('Finger 2 Force')
# axes[1, 0].set_ylabel('Force (N)')
# axes[1, 0].legend(['Fx', 'Fy', 'Fz'])
# axes[1, 0].set_ylim([force_y_min, force_y_max])

# axes[1, 1].plot(range(len(finger2_ee_xyz)), finger2_ee_xyz,  linewidth=LINE_WIDTH)
# axes[1, 1].set_title('Finger 2 End-effector')
# axes[1, 1].set_ylabel('Position (m)')
# axes[1, 1].legend(['Ex', 'Ey', 'Ez'])
# axes[1, 1].set_ylim([ee_y_min, ee_y_max])

# Finger 3 데이터
# axes[2, 0].plot(range(len(finger3_force_xyz)), finger3_force_xyz, linewidth=LINE_WIDTH)
# axes[2, 0].set_title('Finger 3 Force')
# axes[2, 0].set_ylabel('Force (N)')
axes[2, 0].set_xlabel('Time [s]', fontsize=font_size_tick)
axes[2, 0].legend(['Fx', 'Fy', 'Fz'], fontsize=font_size_legend, loc='upper right', frameon=True, facecolor='white')  # Legend 폰트 크기

# axes[2, 0].set_ylim([force_y_min, force_y_max])


# axes[2, 1].plot(range(len(finger3_ee_xyz)), finger3_ee_xyz, linewidth=LINE_WIDTH)
# axes[2, 1].set_title('Finger 3 End-effector')
# axes[2, 1].set_ylabel('Position (m)')
axes[2, 1].set_xlabel('Time [s]', fontsize=font_size_tick)
axes[2, 1].legend(['Ex', 'Ey', 'Ez'], fontsize=font_size_legend, loc='upper right', frameon=True, facecolor='white')  # Legend 폰트 크기
# axes[2, 1].set_ylim([ee_y_min, ee_y_max])

# 레이아웃 조정
plt.tight_layout(rect=[0, 0, 1, 1])  # 전체 제목을 위한 여백
plt.show()
