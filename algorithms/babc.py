import numpy as np


# =========================================================
# ТЕСТОВЫЕ ФУНКЦИИ
# =========================================================

def f1(x):
    return sum(xi ** 2 for xi in x)


def f2(x):
    return sum(
        100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2
        for i in range(len(x) - 1)
    )


def f3(x):
    sum1 = sum(xi ** 2 for xi in x)
    sum2 = sum(np.sin(xi) ** 2 for xi in x)
    f = sum(np.sin(xi) ** 2 for xi in x)
    return (f - np.exp(-sum1)) * np.exp(-sum2)


# =========================================================
# СЛОВАРЬ ВЫБОРА ФУНКЦИЙ
# =========================================================

TEST_FUNCTIONS = {
    "Тестовая функция 1": f1,
    "Тестовая функция 2": f2,
    "Тестовая функция 3": f3,
}


# =========================================================
# ПЕРЕДАТОЧНЫЕ ФУНКЦИИ
# =========================================================

def s1(x):
    return [1 / (1 + np.exp(-2 * xi)) for xi in x]


def s2(x):
    return [1 / (1 + np.exp(-xi)) for xi in x]


def s3(x):
    return [1 / (1 + np.exp(-xi / 2)) for xi in x]


def s4(x):
    return [1 / (1 + np.exp(-xi / 3)) for xi in x]


def v1(x):
    return [
        2 / (1 + np.exp(-2 * xi)) if xi <= 0 else 2 / (1 + np.exp(-2 * xi)) - 1
        for xi in x
    ]


def v2(x):
    return [
        2 / (1 + np.exp(-xi)) if xi <= 0 else 2 / (1 + np.exp(-xi)) - 1
        for xi in x
    ]


def v3(x):
    return [
        2 / (1 + np.exp(-xi / 2)) if xi <= 0 else 2 / (1 + np.exp(-xi / 2)) - 1
        for xi in x
    ]


def v4(x):
    return [
        2 / (1 + np.exp(-xi / 3)) if xi <= 0 else 2 / (1 + np.exp(-xi / 3)) - 1
        for xi in x
    ]


TRANSFER_FUNCTIONS = {
    "S1": s1,
    "S2": s2,
    "S3": s3,
    "S4": s4,
    "V1": v1,
    "V2": v2,
    "V3": v3,
    "V4": v4,
    "VG": v3,
    "SIN": v4
}


# =========================================================
# БИНАРИЗАЦИЯ
# =========================================================

def binarization(x):
    return [1 if xi >= np.random.uniform(0, 1) else 0 for xi in x]


# =========================================================
# BABC АЛГОРИТМ
# =========================================================

class BABC:

    def __init__(self, function_name, transfer_name):
        self.f = TEST_FUNCTIONS[function_name]
        self.transfer = TRANSFER_FUNCTIONS[transfer_name]

    # ---------------- INIT ----------------
    def init(self, s, border, n, threshold):

        points = []

        points.append(np.random.uniform(-border, border, n))

        for i in range(1, s):

            while True:
                x_new = np.random.uniform(-border, border, n)

                ok = True

                for p in points:
                    dist = np.sqrt(np.sum((x_new - p) ** 2))
                    if dist < threshold:
                        ok = False
                        break

                if ok:
                    points.append(x_new)
                    break

        return points

    # ---------------- STEP ----------------
    def step(self, points, b, B, border, P, n, delta):

        results = []

        for p in points:
            x_t = self.transfer(p)
            x_bin = binarization(x_t)
            results.append([self.f(x_bin), p, x_bin])

        results.sort(key=lambda x: x[0])

        new_points = []

        # лучшие области
        for i in range(b):

            base = results[i][1]
            x1 = base - delta
            x2 = base + delta

            for _ in range(B):
                new_points.append(np.random.uniform(x1, x2, n))

        # перспективные области
        for i in range(b, len(results)):

            base = results[i][1]
            x1 = base - delta
            x2 = base + delta

            for _ in range(P):
                new_points.append(np.random.uniform(x1, x2, n))

        # отбор лучших
        results2 = []

        for p in new_points:
            x_t = self.transfer(p)
            x_bin = binarization(x_t)
            results2.append([self.f(x_bin), p, x_bin])

        results2.sort(key=lambda x: x[0])

        return [r[1] for r in results2[:len(points)]], results2

    # ---------------- SOLVE ----------------
    def solve(self, K, s, b, B, P, border, n, delta, threshold):

        points = self.init(s, border, n, threshold)

        for _ in range(K):
            points, results = self.step(points, b, B, border, P, n, delta)

        best = results[0]

        return {
            "best_value": best[0],
            "best_point": best[2]
        }