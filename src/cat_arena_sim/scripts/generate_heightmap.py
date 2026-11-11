#!/usr/bin/env python3
"""Generate the initial 9 m x 5 m sand-bed heightmap for Gazebo Harmonic.

The bed is represented as a static heightmap, not granular sand particles.
Crater geometry is real in the collision heightmap, but excavation/deposition
will be implemented later as a separate terrain-update/quantity model.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

WIDTH = 361
HEIGHT = 201
ARENA_LENGTH = 9.0
ARENA_WIDTH = 5.0
BED_DEPTH = 0.30

# (x, y, radius, depth) in metres. All three lie in the proposed obstacle zone.
CRATERS = [
    (-2.35, 0.90, 0.22, 0.13),
    (-1.05, -1.15, 0.23, 0.18),
    (0.15, 1.25, 0.25, 0.21),
]


def height_at(x: float, y: float) -> float:
    """Return terrain elevation relative to the nominal flat surface z=0."""
    depression = 0.0
    for cx, cy, radius, depth in CRATERS:
        r = math.hypot(x - cx, y - cy)
        if r < radius:
            # Smooth cosine bowl: deepest at the centre, zero slope at rim.
            profile = 0.5 * (1.0 + math.cos(math.pi * r / radius))
            depression = max(depression, depth * profile)
    return -depression


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "models" / "arena_terrain" / "arena_heightmap.pgm"),
        help="Output PGM path",
    )
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    pixels: list[int] = []
    for row in range(HEIGHT):
        # PGM's first row is the top of the image (+Y in this convention).
        y = ARENA_WIDTH / 2.0 - row * ARENA_WIDTH / (HEIGHT - 1)
        for col in range(WIDTH):
            x = -ARENA_LENGTH / 2.0 + col * ARENA_LENGTH / (WIDTH - 1)
            z = height_at(x, y)  # 0 on the flat surface; negative in craters.
            gray = round(255.0 * (z + BED_DEPTH) / BED_DEPTH)
            pixels.append(max(0, min(255, gray)))

    with output.open("w", encoding="ascii") as f:
        f.write(f"P2\n{WIDTH} {HEIGHT}\n255\n")
        for i in range(0, len(pixels), 19):
            f.write(" ".join(map(str, pixels[i : i + 19])) + "\n")

    print(f"Generated {output}")
    print(f"Grid: {WIDTH} x {HEIGHT}; nominal bed depth: {BED_DEPTH:.2f} m")
    for index, (x, y, radius, depth) in enumerate(CRATERS, start=1):
        print(
            f"Crater {index}: centre=({x:.2f}, {y:.2f}) m, "
            f"diameter={2 * radius:.2f} m, depth={depth:.2f} m"
        )


if __name__ == "__main__":
    main()
