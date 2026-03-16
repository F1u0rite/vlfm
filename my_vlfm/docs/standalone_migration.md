# `my_vlfm` 迁移说明（在 vlfm 基座上使用）

如果你要把 `my_vlfm` 单独做仓库，推荐仍将其定位为 **vlfm 上层编排**：

- 运行环境沿用 `vlfm` 依赖
- `vlfm` 保留为底层能力
- `vlfm.integration` 作为兼容门面

## 推荐做法

1. 在新仓库维护 `my_vlfm` 代码。
2. 在部署环境里同时安装 `vlfm` 与 `my_vlfm`。
3. 对历史调用方继续提供 `vlfm.integration` 导出（通过简单转发实现）。

这样能体现“半重构 vlfm”：上层重构、底层保留。
