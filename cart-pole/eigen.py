import numpy as np
from scipy.linalg import solve_continuous_are

# 게인 4개를 주면 뿌리 4개를 돌려준다. 돌려보지 않고 판정하는 것이 목적이다.
# 상태 순서는 어디서나 x, v, theta, omega 로 고정한다.

# TODO 1: 직접 만든 A 표를 옮겨 적는다. 가로도 세로도 x, v, theta, omega 순서다.
A = np.array([
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, -9.81, 0.0],
    [0.0, 0.0, 0.0, 1.0],
    [0.0, 0.0, 19.62, 0.0],
])

# TODO 2: B 줄. 세로 4칸이므로 숫자 4개다.
B = np.array([0.0, 0.1, 0.0, -0.1])


def roots(kx, kv, k, kd):
    """게인 4개를 받아 힘을 켠 뒤의 뿌리 4개를 돌려준다."""
    gains = np.array([kx, kv, k, kd])   # F = kx*x + kv*v + k*theta + kd*omega

    # TODO 3: 힘을 켠 뒤의 표를 만든다.
    #         F 가 각 줄에 미치는 몫은 "B 의 그 칸 × 게인" 이고,
    #         np.outer(B, gains) 가 그 4x4 를 통째로 만들어준다. A 에 더하면 된다.
    closed = A + np.outer(B, gains)

    return np.linalg.eigvals(closed)


def lqr_gains(q_x, q_v, q_theta, q_omega, r):
    """무엇이 얼마나 싫은지를 주면 게인 4개를 계산해서 돌려준다.

    앞의 4개는 상태가 0 에서 벗어난 것이 각각 얼마나 싫은가.
    마지막 r 은 힘을 쓰는 것이 얼마나 싫은가.
    절대값이 아니라 서로의 비율만 의미가 있다.
    """
    Q = np.diag([q_x, q_v, q_theta, q_omega]).astype(float)
    R = np.array([[float(r)]])
    Bcol = B.reshape(4, 1)

    P = solve_continuous_are(A, Bcol, Q, R)
    K = np.linalg.inv(R) @ Bcol.T @ P

    # 교과서는 F = -K·상태 규약이고 hold.py 는 F = +게인·상태 규약이다.
    # 부호를 뒤집지 않으면 게인이 전부 반대로 나와 즉시 넘어진다.
    return -K[0]


# --- 이 아래는 결과를 읽기 좋게 찍는 부분. 계산과 무관 ---

def report(label, kx, kv, k, kd):
    rs = roots(kx, kv, k, kd)
    worst = max(r.real for r in rs)

    print(f"\n{label}")
    print(f"  KX={kx}  KV={kv}  K={k}  KD={kd}")

    for r in sorted(rs, key=lambda z: -z.real):
        shape = "커진다" if r.real > 1e-9 else ("사그라든다" if r.real < -1e-9 else "그대로")
        swing = " · 흔들린다" if abs(r.imag) > 1e-9 else ""
        print(f"    {r.real:9.4f} {r.imag:+9.4f}i    {shape}{swing}")

    if worst > 1e-9:
        print("    → 불안정. 이 조합으로는 안 선다")
    elif worst > -1e-9:
        print("    → 경계. 줄지도 늘지도 않는다")
    else:
        print(f"    → 안정. 가장 느린 뿌리 {worst:.4f} · 대략 {4 / -worst:.1f}초 걸린다")


if __name__ == "__main__":
    report("힘 없음 (2주차)", 0, 0, 0, 0)
    report("각도만 (3주차)", 0, 0, 200, 0.05)
    report("게인 4개 (4주차)", 10, 50, 400, 100)
    report("K 를 벽 바로 위로", 10, 50, 197, 100)

    report("KX 2배", 20, 50, 400, 100)
    report("KV 2배", 10, 100, 400, 100)
    report("K 2배",  10, 50, 800, 100)
    report("KD 2배", 10, 50, 400, 200)

    # TODO 4: Q 와 R 을 정한다. 게인이 아니라 "무엇이 얼마나 싫은가" 를 정하는 것이다.
    #         앞 4개는 x, v, theta, omega 순서이고 마지막이 힘이다.
    #         전부 1 로 시작해서 하나씩 바꿔가며 뿌리가 어디로 가는지 본다.
    g = lqr_gains(100, 10, 1, 1, 1)
    print(f"\nLQR 이 뽑은 게인: KX={g[0]:.2f} KV={g[1]:.2f} K={g[2]:.2f} KD={g[3]:.2f}")
    report("LQR", *g)