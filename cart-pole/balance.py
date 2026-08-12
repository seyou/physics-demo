import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 막대 세우기. 물리는 sim.py 와 같고, F 를 매 스텝 정하는 것만 다르다.

# --- 물리 상수 ---
G = 9.81        # 중력가속도 (m/s^2)
L = 1.0         # 막대 길이 (m)
M_CART = 10.0    # 카트 질량 (kg)
M_POLE = 10.0    # 추 질량 (kg)
DT = 0.005      # 시간 간격 (s)

K = 200.0         # TODO 1: 제어 게인. 부호와 크기를 정한다.
KD = 0.05

def step(x, v, theta, omega):
    """상태 4개를 받아 DT 만큼 지난 다음 상태 4개를 돌려준다.

    x     : 카트 위치 (오른쪽이 +)
    v     : 카트 속도
    theta : 막대 각도 (라디안, 똑바로 선 상태가 0, 오른쪽으로 기울면 +)
    omega : 각속도
    """
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    # TODO 2: 카트를 미는 힘. theta 하나만 보고 정한다. 오른쪽으로 미는 것이 +.
    force = K * theta + KD * omega

    # TODO 3: 아래는 F = 0 일 때의 식이다. 2주차 유도에 있던 F 항을 되살린다.
    #         분자에 `- force * cos_t` 가 들어간다.
    alpha = (((M_CART + M_POLE) * G * sin_t)
             - (M_POLE * L * omega**2 * sin_t * cos_t) - (force * cos_t)) / (L * (M_CART + M_POLE * sin_t**2))

    # TODO 4: 카트 가속도 (A) 식에도 F 가 들어간다. 분자에 `force +` 가 붙는다.
    a = (M_POLE * L * (omega**2 * sin_t - alpha * cos_t) + force) / (M_CART + M_POLE)

    new_omega = omega + alpha * DT
    new_theta = theta + new_omega * DT
    new_v = v + a * DT
    new_x = x + new_v * DT

    return new_x, new_v, new_theta, new_omega


# --- 초기 상태: 1도 기울인 채 가만히 놓는다 ---
state = (0.0, 0.0, math.radians(-1), 0.0)


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

    # 관찰: 막대가 몇 도 기울었고 카트가 어디까지 갔는가
    print(f"{math.degrees(theta):8.2f}도  x={x:7.3f}")

    cart.set_data([x], [0])
    rod.set_data([x, bob_x], [0, bob_y])
    return cart, rod


ani = FuncAnimation(fig, frame, interval=10, blit=True, cache_frame_data=False)
plt.show()
