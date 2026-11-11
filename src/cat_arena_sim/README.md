# Caterpillar Autonomy Challenge — Arena World v0.1

This starter world is for **ROS 2 Jazzy + Gazebo Harmonic**.

## Included

- 9 m x 5 m arena footprint.
- Static heightmap bed representing a nominal 0.30 m sand layer.
- Three collision craters in the obstacle zone (0.44–0.50 m diameter, varying depth).
- Three 0.32–0.40 m obstacle-zone boulders with varying ellipsoid heights.
- One smaller optional boulder in the excavation zone.
- Proposed start, obstacle, excavation, construction, and berm-target markings.
- Boundary walls for simulation containment only.

## Important modelling assumptions

The rulebook gives the arena footprint, nominal sand depth, minimum obstacle counts, and obstacle dimensions. It does **not** give exact zone coordinates in the text, so the zone boundaries and target-strip coordinates in this prototype are configurable assumptions, not official competition dimensions.

The sand is currently a static heightmap with approximate contact friction. This is **not** a granular-particle sand simulation. Excavation, carrying, and deposition will be implemented later as robot mechanisms plus a terrain/volume bookkeeping model.

The walls are only a safety boundary in simulation. The robot's mapping, localization, and obstacle-avoidance stack must not use them as navigation references, in accordance with the competition rules.

## Install into your workspace

Copy the `cat_arena_sim` folder into `~/cat_autonomy_ws/src/`.

```bash
cd ~/cat_autonomy_ws
colcon build --packages-select cat_arena_sim --symlink-install
source install/setup.bash
export GZ_SIM_RESOURCE_PATH="$HOME/cat_autonomy_ws/src/cat_arena_sim/models:${GZ_SIM_RESOURCE_PATH}"
gz sim -v 3 src/cat_arena_sim/worlds/moon_yard_world.sdf
```

If `gz sim --version` is unavailable, install Gazebo Harmonic before running the world.

## Regenerate the terrain heightmap

```bash
python3 src/cat_arena_sim/scripts/generate_heightmap.py
```

The three crater centres and dimensions are defined near the top of that script.
