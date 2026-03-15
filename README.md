# ljie_pipeline

这是一个面向**单细胞（scRNA-seq）/多组学（multi-omics）/空间组学（spatial omics）**分析的双语言仓库模板，支持 **R + Python** 协同开发。

## 1. 你能用它做什么
- 用 **Python** 进行数据预处理、批次校正、整合分析、可视化自动化。
- 用 **R**（Seurat / Signac / Bioconductor）进行常见单细胞和空间分析工作流。
- 在同一仓库中统一管理：
  - 原始数据与结果目录
  - 参数配置
  - 文档与复现命令

## 2. 仓库结构
```text
.
├── configs/                 # 分析参数（样本信息、过滤阈值、模型参数）
├── data/
│   ├── raw/                 # 原始数据（默认不入库）
│   ├── processed/           # 中间处理结果
│   └── results/             # 最终结果（图表、marker、统计报告）
├── docs/                    # 方法说明、学习路径、分析记录
├── python/
│   ├── scripts/             # Python CLI 脚本入口
│   ├── src/omics_pipeline/  # Python 业务模块
│   └── tests/               # Python 单元测试
├── R/
│   └── scripts/             # R 分析脚本入口
└── scripts/
    └── bootstrap_python.sh  # 一键初始化 Python 环境
```

## 3. 快速开始

### 3.1 Python 一键初始化
```bash
bash scripts/bootstrap_python.sh
source .venv/bin/activate
```

### 3.2 R 环境（建议）
```r
install.packages(c("Seurat", "Signac", "tidyverse", "patchwork", "yaml"))
```

> 后续建议使用 `renv` 锁定依赖，确保分析可复现。

## 4. 常用命令
```bash
# 基础检查：编译 + 单元测试 + 模板运行
make smoke-python

# 单独运行 Python 模板流程
python python/scripts/run_python_pipeline.py --config configs/project.example.yaml

# 单独运行 R 模板流程
Rscript R/scripts/run_r_pipeline.R configs/project.example.yaml
```

## 5. 下一步建议（面向真实项目）
1. 把你的样本信息填入 `configs/project.example.yaml` 并另存为 `configs/project.yaml`。
2. 先跑一批小样本，验证目录输出是否符合预期。
3. 再把真实分析步骤逐步替换到 `python/src/omics_pipeline/` 和 `R/scripts/`。
4. 每做一次关键分析，记录在 `docs/analysis-log.md`。
5. 参考 `docs/next-steps-cn.md` 执行逐步落地。

## 6. 注意事项
- 本模板不直接包含你的原始测序数据。
- 真实项目中请添加伦理与数据权限说明。
- 建议为每个里程碑打 tag（例如 `v0.1-qc-done`）。
