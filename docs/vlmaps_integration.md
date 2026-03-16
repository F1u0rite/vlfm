# VLMaps 接入 VLFM 的输入输出与模块边界

本文档定义一个可落地的最小集成方案：`语言指令 -> 语义查询 -> 目标点生成 -> A*路径规划 -> 导航状态输出`。

## 架构调整（按你的要求）

- 新上层仓库（repo-style）：`my_vlfm/`
  - 放置任务编排逻辑与输入输出定义
- 现有底层库：`vlfm/`
  - 作为底层接口使用
  - `vlfm.integration` 仅保留兼容转发层（调用 `my_vlfm`）

## 输入定义

1. **自然语言指令**
   - 示例：`go to the chair near the door`
2. **机器人位姿**
   - 2D：`(x, y, yaw)`（当前状态机使用 `(x, y)` 做路径规划）
3. **语义地图（VLMaps）**
   - 每个语义区域包含 `category` 与 `Nx2` 地图坐标点集
4. **占据栅格地图**
   - `0=free, 1=obstacle, 2=unknown`

## 输出定义

1. **目标语义区域**
   - 被选中的 `SemanticRegion`
2. **导航目标点**
   - `goal_point: (x_goal, y_goal)`
3. **导航状态**
   - `searching / goal selected / path planned / arrived / failed`
4. **规划路径**
   - waypoints 列表（地图坐标系）

## 对应代码模块

- 上层实现（主）：
  - `my_vlfm/my_vlfm/language_parser.py`
  - `my_vlfm/my_vlfm/semantic_map.py`
  - `my_vlfm/my_vlfm/goal_selector.py`
  - `my_vlfm/my_vlfm/planner.py`
  - `my_vlfm/my_vlfm/navigation_state_machine.py`
- 兼容接口（底层库对外门面）：
  - `vlfm/integration/*.py`（全部转发到 `my_vlfm`）

## 设计原则

- **上层（my_vlfm）决定去哪（语义目标）**
- **规划器（A* / Nav2）决定怎么去（几何路径）**
- **底层（vlfm）提供能力基座与兼容接口**

这样可以把任务逻辑和底层能力分离，便于后续独立维护 `my_vlfm`。
