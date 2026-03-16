# my_vlfm 架构

## 定位
- `vlfm`：底层能力库
- `my_vlfm`：上层任务编排包
- `vlfm.integration`：兼容门面，转发到 `my_vlfm`

## 处理链路
1. `scene_export` 读取（occupancy/semantic/metadata）
2. `LanguageParser`
3. `SemanticMap` 查询
4. `GoalSelector`
5. `AStarPlanner`
6. `NavigationStateMachine` 输出状态

## 模块
- `scene_export.py`
- `language_parser.py`
- `semantic_map.py`
- `goal_selector.py`
- `planner.py`
- `navigation_state_machine.py`

## 关键参数
- `free_value`：占据图中可通行编码（你的规范通常为 1）
- `unknown_value`：未知区域编码（通常为 2）
