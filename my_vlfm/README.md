# my_vlfm

`my_vlfm` 是一个可单独使用的上层语义导航包，负责：

- 语言指令解析
- 语义地图查询
- 目标点生成
- A* 路径规划
- 导航状态机编排

`my_vlfm` 不依赖 `vlfm.integration`，可以直接作为独立包安装与使用。

## 快速使用

```python
from my_vlfm import NavigationStateMachine, SemanticMap
```

## 目录

- `my_vlfm/*.py`：核心模块
- `tests/`：包级测试
- `docs/architecture.md`：架构说明

## 独立仓库迁移

可参考 `docs/standalone_migration.md` 将 `my_vlfm/` 直接迁移到独立仓库。
