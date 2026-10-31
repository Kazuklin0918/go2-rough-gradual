from mjlab.tasks.registry import register_mjlab_task
from src.tasks.velocity.rl import VelocityOnPolicyRunner

from .env_cfgs import (
  unitree_go2_flat_env_cfg,
  unitree_go2_rough_env_cfg,
)
from .rl_cfg import unitree_go2_ppo_runner_cfg

register_mjlab_task(
  task_id="Unitree-Go2-Rough",
  env_cfg=unitree_go2_rough_env_cfg(),
  play_env_cfg=unitree_go2_rough_env_cfg(play=True),
  rl_cfg=unitree_go2_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Unitree-Go2-Flat",
  env_cfg=unitree_go2_flat_env_cfg(),
  play_env_cfg=unitree_go2_flat_env_cfg(play=True),
  rl_cfg=unitree_go2_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

# Added for the PAI final assignment: widen the velocity command range in 4 steps instead of 1 (Rough only).
_GRADUAL_VELOCITY_STAGES = [
  {"step": 0, "lin_vel_x": (-0.5, 1.0), "lin_vel_y": (-0.5, 0.5), "ang_vel_z": (-1.0, 1.0)},
  {"step": 4000 * 24, "lin_vel_x": (-0.6, 1.25), "lin_vel_y": (-0.6, 0.6)},
  {"step": 5500 * 24, "lin_vel_x": (-0.75, 1.5), "lin_vel_y": (-0.75, 0.75)},
  {"step": 7000 * 24, "lin_vel_x": (-0.9, 1.75), "lin_vel_y": (-0.9, 0.9)},
  {"step": 8500 * 24, "lin_vel_x": (-1.0, 2.0), "lin_vel_y": (-1.0, 1.0)},
]


def unitree_go2_rough_gradual_env_cfg(play: bool = False):
  cfg = unitree_go2_rough_env_cfg(play=play)
  if "command_vel" in cfg.curriculum:
    cfg.curriculum["command_vel"].params["velocity_stages"] = _GRADUAL_VELOCITY_STAGES
  return cfg


register_mjlab_task(
  task_id="Unitree-Go2-Rough-Gradual",
  env_cfg=unitree_go2_rough_gradual_env_cfg(),
  play_env_cfg=unitree_go2_rough_gradual_env_cfg(play=True),
  rl_cfg=unitree_go2_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)
