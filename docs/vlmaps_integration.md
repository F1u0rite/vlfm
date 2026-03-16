# VLMaps 接入方案：my_vlfm 输入输出与模块边界

本文档定义一个可落地的最小集成方案：`语言指令 -> 语义查询 -> 目标点生成 -> A*路径规划 -> 导航状态输出`。

## 架构

- 上层包：`my_vlfm/`
- 底层能力：`vlfm/`
- 兼容接口：`vlfm.integration`（转发到 `my_vlfm`）

## 你的 `scene_export/` 目录（已适配）

```text
scene_export/
├─ occupancy_map.npy
├─ occupancy_map.png
├─ semantic_objects.json
├─ semantic_points.json
├─ topdown_rgb_map.png
├─ map_metadata.json
└─ export_readme.txt
```

`my_vlfm.scene_export` 可直接读取：
- `load_scene_export(scene_export_dir)`：读取 metadata + occupancy + semantic map
- `infer_occupancy_labels(metadata)`：从 `occupancy_label_def` 推断 free/unknown 编码

## 输入定义

1. 自然语言指令（如 `go to the chair near the door`）
2. 机器人位姿（当前状态机使用 `(x, y)`）
3. 语义地图（由 `semantic_objects.json` 或 `semantic_points.json` 读取）
4. 占据栅格（`occupancy_map.npy`）

## 输出定义

1. 目标语义区域（`SemanticRegion`）
2. 导航目标点（`goal_point: (x_goal, y_goal)`）
3. 导航状态（`path planned / arrived / failed`）
4. 规划路径（waypoints）

## 关键编码兼容

你的规范里 occupancy 编码是：
- `0 = obstacle`
- `1 = free`
- `2 = unknown`

`my_vlfm` 的 `AStarPlanner` / `GoalSelector` 现已支持 `free_value`、`unknown_value` 参数，因此可直接对齐该编码。

## 对应代码模块（my_vlfm）

- `my_vlfm/scene_export.py`（读取 scene_export）
- `my_vlfm/language_parser.py`
- `my_vlfm/semantic_map.py`
- `my_vlfm/goal_selector.py`
- `my_vlfm/planner.py`
- `my_vlfm/navigation_state_machine.py`

## 设计原则

- 上层（my_vlfm）决定去哪（语义目标）
- 规划器（A* / Nav2）决定怎么去（几何路径）
- 底层（vlfm）提供能力基座与兼容入口
