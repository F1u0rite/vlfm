# my_vlfm

`my_vlfm` 是一个可单独使用的上层语义导航包，负责：

- 语言指令解析
- 语义地图查询
- 目标点生成
- A* 路径规划
- 导航状态机编排

`my_vlfm` 以上层编排为主，建议在 `vlfm` 环境中使用；同时保留 `vlfm.integration` 兼容导出，便于把它作为 vlfm 的半重构上层。

## 快速使用

```python
from my_vlfm import NavigationStateMachine, SemanticMap
```

## 目录

- `my_vlfm/*.py`：核心模块
- `tests/`：包级测试
- `docs/architecture.md`：架构说明

## 与 vlfm 的关系

- `vlfm` 作为底层能力与历史接口
- `my_vlfm` 作为上层语义任务编排
- 通过 `vlfm.integration` 兼容层可继续按 `vlfm` 路径使用新能力
