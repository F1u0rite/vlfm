# my_vlfm

`my_vlfm` 是面向任务编排的上层语义导航仓库（repo-style 目录）。

- `vlfm` 作为底层能力库（感知/地图/策略基础组件）
- `my_vlfm` 作为上层任务接口（语言解析、语义查询、目标点生成、路径规划、状态机）

## 目录

- `my_vlfm/`：核心 Python 包
- `tests/`：上层逻辑测试
- `docs/`：架构说明

## 与 vlfm 的关系

当前工程中 `vlfm.integration` 已改为兼容接口层，内部转发到 `my_vlfm`。
这样可以把 `vlfm` 当底层库使用，同时将任务逻辑集中在 `my_vlfm`。
