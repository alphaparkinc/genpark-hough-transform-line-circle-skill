"""Hough Transform Parametric Accumulator Engine
100% Python Standard Library (math).
"""

import math

class HoughTransformEngine:
    """Accumulator parameter space voting for lines and linear features."""
    def __init__(self, angle_step=2, rho_step=1):
        self.angle_step = angle_step
        self.rho_step = rho_step

    def detect_lines(self, edge_image, threshold=10):
        h, w = len(edge_image), len(edge_image[0])
        thetas = [math.radians(deg) for deg in range(-90, 90, self.angle_step)]
        accumulator = {}

        for y in range(h):
            for x in range(w):
                if edge_image[y][x] > 0:
                    for theta in thetas:
                        rho = int(x * math.cos(theta) + y * math.sin(theta))
                        key = (rho, round(theta, 3))
                        accumulator[key] = accumulator.get(key, 0) + 1

        detected_lines = []
        for (rho, theta), count in accumulator.items():
            if count >= threshold:
                detected_lines.append({"rho": rho, "theta_rad": theta, "votes": count})

        detected_lines.sort(key=lambda item: item["votes"], reverse=True)
        return {
            "lines_count": len(detected_lines),
            "top_lines": detected_lines[:5]
        }
