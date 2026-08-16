import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 카트까지 제자리에 붙잡기. 물리는 balance.py 와 같고, force 한 줄만 다르다.

# --- 물리 상수 ---
G = 9.81        # 중력가속도 (m/s^2)
L = 1.0         # 막대 길이 (m)
M_CART = 10.0   # 카트 질량 (kg)
M_POLE = 10.0   # 추 질량 (kg)
DT = 0.005      # 시간 간격 (s)

# --- 제어 게인 ---
K = 422.33       # 각도
KD = 98.67       # 각속도
KX = 1.0        # TODO 1: 카트 위치. 부호와 크기를 정한다.
KV = 6.86        # TODO 2: 카트 속도. 부호와 크기를 정한다.

def step(x, v, theta, omega):
    """상태 4개를 받아 DT 만큼 지난 다음 상태 4개를 돌려준다.

    x     : 카트 위치 (오른쪽이 +)
    v     : 카트 속도
    theta : 막대 각도 (라디안, 똑바로 선 상태가 0, 오른쪽으로 기울면 +)
    omega : 각속도
    """
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    # TODO 3: 아래는 각도만 보는 3주차 힘이다. x 와 v 를 보는 항을 더한다.
    #         부호는 직접 정한다 — 지난주에 본 "왼쪽으로 가려면 먼저 오른쪽으로 민다" 가
    #         여기서 부호로 나타난다.
    force = K * theta + KD * omega + KX * x + KV * v

    alpha = (((M_CART + M_POLE) * G * sin_t)
             - (M_POLE * L * omega**2 * sin_t * cos_t) - (force * cos_t)) / (L * (M_CART + M_POLE * sin_t**2))

    a = (M_POLE * L * (omega**2 * sin_t - alpha * cos_t) + force) / (M_CART + M_POLE)

    new_omega = omega + alpha * DT
    new_theta = theta + new_omega * DT
    new_v = v + a * DT
    new_x = x + new_v * DT

    return new_x, new_v, new_theta, new_omega


# --- 초기 상태: 막대는 똑바로 선 채, 카트만 0.5 m 오른쪽에 놓는다 ---
state = (0.5, 0.0, 0.0, 0.0)


# --- 이 아래는 그림 그리는 부분. 물리와 무관 ---
fig, ax = plt.subplots()
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axhline(0, color="0.85", lw=1)                    # 레일
ax.axvline(0, color="0.85", lw=1)                    # 목표 위치
cart, = ax.plot([], [], "s", markersize=22)
rod, = ax.plot([], [], "o-", lw=2, markersize=10)


def frame(_):
    global state
    state = step(*state)
    x, v, theta, omega = state

    bob_x = x + L * math.sin(theta)
    bob_y = L * math.cos(theta)

    # 관찰: 막대가 몇 도 기울었고 카트가 0 으로 돌아오는가
    print(f"{math.degrees(theta):8.2f}도  x={x:7.3f}")

    cart.set_data([x], [0])
    rod.set_data([x, bob_x], [0, bob_y])
    return cart, rod


ani = FuncAnimation(fig, frame, interval=10, blit=True, cache_frame_data=False)
plt.show()
