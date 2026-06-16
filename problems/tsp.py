import math


class TSP:
    def __init__(self, cities):
        """
        cities:
        [
            (1, x1, y1),
            (2, x2, y2),
            ...
        ]
        """

        self.cities = cities
        self.n = len(cities)

        self.distance_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self):

        matrix = []

        for i in range(self.n):

            row = []

            for j in range(self.n):

                if i == j:
                    row.append(0.0)

                else:

                    x1 = self.cities[i][1]
                    y1 = self.cities[i][2]

                    x2 = self.cities[j][1]
                    y2 = self.cities[j][2]

                    distance = math.sqrt(
                        (x2 - x1) ** 2 +
                        (y2 - y1) ** 2
                    )

                    row.append(distance)

            matrix.append(row)

        return matrix

    def route_length(self, route):

        total_distance = 0.0

        for i in range(len(route) - 1):
            city1 = route[i] - 1
            city2 = route[i + 1] - 1

            total_distance += (
                self.distance_matrix[city1][city2]
            )

        return total_distance

# =========================================================
if __name__ == "__main__":

    cities = [
        (1, 10, 15),
        (2, 25, 30),
        (3, 40, 12),
        (4, 55, 45),
        (5, 70, 20)
    ]

    tsp = TSP(cities)

    print("Матрица расстояний:")

    for row in tsp.distance_matrix:
        print(row)

    route = [1, 3, 2, 5, 4, 1]

    print()
    print("Маршрут:")
    print(route)

    print()
    print("Длина маршрута:")
    print(tsp.route_length(route))