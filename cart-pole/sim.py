import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 물리 상수 ---
G = 9.81        # 중력가속도 (m/s^2)
L = 1.0         # 막대 길이 (m)
M_CART = 1.0    # 카트 질량 (kg)
M_POLE = 1.0    # 추 질량 (kg)
DT = 0.005      # 시간 간격 (s)

initial_com = None
max_error = 0.0

def step(x, v, theta, omega):
    """상태 4개를 받아 DT 만큼 지난 다음 상태 4개를 돌려준다.

    x     : 카트 위치 (오른쪽이 +)
    v     : 카트 속도
    theta : 막대 각도 (라디안, 똑바로 선 상태가 0, 오른쪽으로 기울면 +)
    omega : 각속도
    """
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    # TODO 1: 각가속도. 위에서 유도한 θ̈ 식을 그대로 옮긴다.
    #         F = 0 이므로 F 항은 빠진다.
    alpha = (((M_CART + M_POLE) * G * sin_t) - (M_POLE * L * omega**2 * sin_t * cos_t)) / (L * (M_CART + M_POLE * sin_t**2))

    # TODO 2: 카트 가속도. (A) 식이다. TODO 1 의 alpha 가 필요하므로 순서가 중요하다.
    a = (M_POLE * L * (omega**2 * sin_t - alpha * cos_t)) / (M_CART + M_POLE)

    # TODO 3: 준암시적 오일러로 4개를 갱신한다.
    #         1주차 교훈 — 위치 갱신에는 "새로 구한" 속도를 쓴다.
    new_omega = omega + alpha * DT
    new_theta = theta + new_omega * DT
    new_v = v + a * DT
    new_x = x + new_v * DT

    return new_x, new_v, new_theta, new_omega

# 가속도가 속도를 바꾸고, 속도가 위치를 바꾼다.

# --- 초기 상태: 5도 기울인 채 가만히 놓는다 ---
state = (0.0, 0.0, math.radians(5), 0.0)


# --- 이 아래는 그림 그리는 부분. 물리와 무관 ---
fig, ax = plt.subplots()
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect("equal")
ax.axhline(0, color="0.85", lw=1)                    # 레일
cart, = ax.plot([], [], "s", markersize=22)
rod, = ax.plot([], [], "o-", lw=2, markersize=10)


def frame(_):
    global state
    state = step(*state)
    x, v, theta, omega = state

    bob_x = x + L * math.sin(theta)
    bob_y = L * math.cos(theta)

    # TODO 4 (검증용): 카트와 추의 무게중심 x 를 구해 찍어본다.
    #         질량가중 평균이다. F = 0 이므로 이 값은 처음 값에서 변하면 안 된다.
    # print ((M_CART * x + M_POLE * bob_x) / (M_CART + M_POLE))

    global initial_com, max_error

    com = (M_CART * x + M_POLE * bob_x) / (M_CART + M_POLE)

    if initial_com is None:
        initial_com = com

    error = abs(com - initial_com)
    if error > max_error:
        max_error = error
    print(f"{max_error:.6f}")


    cart.set_data([x], [0])
    rod.set_data([x, bob_x], [0, bob_y])
    return cart, rod


ani = FuncAnimation(fig, frame, interval=10, blit=True, cache_frame_data=False)
plt.show()