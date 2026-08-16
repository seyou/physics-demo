import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from eigen import lqr_gains

# 아래로 늘어진 막대를 흔들어 올려서 세운다.
#
# 물리는 hold.py 와 똑같다. 달라지는 것은 두 가지뿐이다.
#   1. 시작 각도가 180도 (막대가 아래로 늘어져 있다)
#   2. force 가 두 개로 갈린다 — 올리는 힘과 잡는 힘

# --- 물리 상수 (hold.py 와 동일) ---
G = 9.81        # 중력가속도 (m/s^2)
L = 1.0         # 막대 길이 (m)
M_CART = 10.0   # 카트 질량 (kg)
M_POLE = 10.0   # 추 질량 (kg)
DT = 0.005      # 시간 간격 (s)

# --- 직립 근방을 맡을 게인. 5주차 결과를 그대로 가져온다 ---
KX, KV, K, KD = lqr_gains(100, 10, 1, 1, 1)


# TODO 1: 지금 이 순간 막대가 가진 에너지를 돌려준다.
#         운동에너지 T 와 위치에너지 V 를 더하면 된다.
#         이것을 적는 것이 곧 라그랑주의 1단계이기도 하다 — 여기서 나온 T, V 로
#         운동방정식을 다시 유도해 2주차 뉴턴 결과와 대조한다.
#         기준점은 자유롭게 잡아도 되지만, 어디로 잡았는지는 TODO 2 와 맞아야 한다.
def energy(theta, omega):
    return 0.0


# TODO 2: 막대가 똑바로 섰을 때의 에너지.
#         TODO 1 의 식에 theta=0, omega=0 을 넣은 값이다. 목표선이다.
E_UP = 0.0


# TODO 3: 올리는 힘.
#         지금 에너지가 E_UP 에 모자라면 넣어주고, 넘치면 빼야 한다.
#         어려운 것은 크기가 아니라 방향이다 — 카트를 어느 쪽으로 밀어야
#         막대에 에너지가 "들어가는가". 그네를 밀어본 기억이 답에 가깝고,
#         식에서는 막대가 도는 방향(omega)이 그걸 알려준다.
def swing_force(x, v, theta, omega):
    return 0.0


# TODO 4: 언제 LQR 에게 넘길 것인가.
#         너무 일찍 넘기면 소각도 밖이라 LQR 이 못 잡고,
#         너무 늦게 넘기면 막대가 꼭대기를 그냥 지나쳐 버린다.
#         각도만 볼지, 각속도까지 볼지 정한다.
#
#         주의: theta 는 계속 돌기 때문에 370도, 730도처럼 한없이 커진다.
#         "0도 근처인가" 를 그냥 비교하면 두 바퀴째부터 안 걸린다.
def is_near_upright(theta, omega):
    return False


def control(x, v, theta, omega):
    """올리는 힘과 잡는 힘 중 하나를 고른다."""
    if is_near_upright(theta, omega):
        return KX * x + KV * v + K * theta + KD * omega
    return swing_force(x, v, theta, omega)


def step(x, v, theta, omega):
    """상태 4개를 받아 DT 만큼 지난 다음 상태 4개를 돌려준다."""
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)

    force = control(x, v, theta, omega)

    alpha = (((M_CART + M_POLE) * G * sin_t)
             - (M_POLE * L * omega**2 * sin_t * cos_t)
             - (force * cos_t)) / (L * (M_CART + M_POLE * sin_t**2))

    a = (M_POLE * L * (omega**2 * sin_t - alpha * cos_t) + force) / (M_CART + M_POLE)

    new_omega = omega + alpha * DT
    new_theta = theta + new_omega * DT
    new_v = v + a * DT
    new_x = x + new_v * DT

    return new_x, new_v, new_theta, new_omega


# --- 초기 상태: 막대가 아래로 늘어진 채 가만히 있다 ---
state = (0.0, 0.0, math.pi, 0.0)


# --- 이 아래는 그림 그리는 부분. 물리와 무관 ---
fig, ax = plt.subplots()
ax.set_xlim(-2.5, 2.5)
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

    # 관찰: 에너지가 목표선에 다가가는가, 그리고 막대가 꼭대기에 붙는가
    deg = math.degrees(theta) % 360
    print(f"{deg:7.1f}도  E={energy(theta, omega):8.2f} / {E_UP:.2f}  x={x:7.3f}")

    cart.set_data([x], [0])
    rod.set_data([x, bob_x], [0, bob_y])
    return cart, rod


ani = FuncAnimation(fig, frame, interval=10, blit=True, cache_frame_data=False)
plt.show()
