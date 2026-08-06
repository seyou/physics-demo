import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 물리 상수 ---
G = 9.81      # 중력가속도 (m/s^2)
L = 1.0       # 막대 길이 (m)
DT = 0.01     # 시간 간격 (s)


def step(theta, omega):
    """현재 상태를 받아 DT 만큼 지난 다음 상태를 돌려준다.

    theta: 각도 (라디안, 아래로 늘어진 상태가 0)
    omega: 각속도 (theta 의 시간 변화율)
    """

    # print(0.5 * L**2 * omega**2 + G * L * (1 - math.cos(theta)))

    # TODO 1: 지금 각도에서 각가속도를 구한다.   θ̈ = −(g/l) sin θ
    alpha = -(G / L) * math.sin(theta)

    # TODO 2: 가속도로 각속도를 갱신한다
    new_omega = omega + (alpha * DT)

    # TODO 3: 각속도로 각도를 갱신한다
    # new_theta = theta + (omega * DT)  --> 각이 점점 커짐
    new_theta = theta + (new_omega * DT)

    return new_theta, new_omega

# --- 초기 상태: 30도에서 가만히 놓는다 ---
state = (math.radians(30), 0.0)

# --- 이 아래는 그림 그리는 부분. 물리와 무관 ---
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 0.5)
ax.set_aspect("equal")
rod, = ax.plot([], [], "o-", lw=2, markersize=12)


def frame(_):
    global state
    state = step(*state)
    theta, _ = state
    x = L * math.sin(theta)      # 핀에서 추까지의 가로 거리
    y = -L * math.cos(theta)     # 세로 거리 (아래가 음수)
    rod.set_data([0, x], [0, y])
    return (rod,)


FuncAnimation(fig, frame, interval=10, blit=True, cache_frame_data=False)
plt.show()