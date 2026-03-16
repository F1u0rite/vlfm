# my_vlfm 架构

## 定位
- `vlfm`：底层能力库
- `my_vlfm`：上层任务编排包
- `vlfm.integration`：兼容门面，转发到 `my_vlfm`

## 处理链路
1. `LanguageParser`
2. `SemanticMap` 查询
3. `GoalSelector`
4. `AStarPlanner`
5. `NavigationStateMachine` 输出状态

## 模块
- `language_parser.py`
- `semantic_map.py`
- `goal_selector.py`
- `planner.py`
- `navigation_state_machine.py`
