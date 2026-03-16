# my_vlfm

`my_vlfm` 是上层语义导航编排包，负责：

- 语言指令解析
- 语义地图查询
- 目标点生成
- A* 路径规划
- 导航状态机编排

建议在 `vlfm` 环境中使用；`vlfm.integration` 提供兼容导出。

## 快速使用（对接 scene_export）

```python
from my_vlfm import (
    NavigationStateMachine,
    infer_occupancy_labels,
    load_scene_export,
)

bundle = load_scene_export("scene_export")
free_value, unknown_value = infer_occupancy_labels(bundle.metadata)

sm = NavigationStateMachine(
    semantic_map=bundle.semantic_map,
    occupancy_grid=bundle.occupancy_map,
    meters_per_cell=bundle.metadata.cell_size_m,
    free_value=free_value,
    unknown_value=unknown_value,
)

result = sm.run("go to the chair near the door", robot_xy=(1.0, 2.0))
print(result.state, result.goal_point)
```

## 与 vlfm 的关系

- `vlfm`：底层能力与历史接口
- `my_vlfm`：上层语义任务编排
- `vlfm.integration`：兼容层（转发到 `my_vlfm`）
