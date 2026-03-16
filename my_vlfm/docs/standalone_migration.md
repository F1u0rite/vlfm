# 将 `my_vlfm` 拆分为独立仓库（推荐流程）

下面是把当前目录中的 `my_vlfm/` 迁移成独立仓库的最小步骤。

## 1. 创建新仓库并复制目录

```bash
mkdir -p ~/my_vlfm_repo
cp -r /path/to/vlfm/my_vlfm/* ~/my_vlfm_repo/
cd ~/my_vlfm_repo
```

## 2. 初始化 git（如果是全新仓库）

```bash
git init
git add .
git commit -m "Initial standalone my_vlfm package"
```

## 3. 安装并验证

```bash
pip install -e .
python -c "from my_vlfm import NavigationStateMachine, SemanticMap; print('ok')"
```

## 4. 与 vlfm 的关系

- `my_vlfm` 可以独立运行。
- 若你希望复用 `vlfm` 的底层能力，只需在同一 Python 环境中安装 `vlfm` 即可。
- 不再依赖 `vlfm.integration`（该层已删除）。
