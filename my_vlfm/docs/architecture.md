# my_vlfm 架构

## 定位
- `my_vlfm`：上层任务编排仓库
- `vlfm`：底层能力库（被上层调用）

## 处理链路
1. `LanguageParser`
2. `SemanticMap` 查询
3. `GoalSelector`
4. `AStarPlanner`
5. `NavigationStateMachine` 输出状态

## 兼容策略
为了不影响旧代码：
- `vlfm.integration` 仍可 import
- 但内部实现全部转发到 `my_vlfm`
