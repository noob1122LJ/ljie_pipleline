# 下一步执行清单（给你现在就能用）

## 1) 先把环境跑起来（Python）
```bash
bash scripts/bootstrap_python.sh
source .venv/bin/activate
make smoke-python
```

## 2) 填写真实项目配置
- 复制 `configs/project.example.yaml` 为 `configs/project.yaml`
- 修改 `project.name / species / owner`
- 把 `samples` 里的 `sample_id / modality / path` 换成你的真实样本

## 3) 准备数据目录
- 原始数据放 `data/raw/<sample_id>/`
- 中间结果会输出到 `data/processed/`
- 最终结果会输出到 `data/results/`

## 4) 逐步替换模板逻辑
- Python：在 `python/src/omics_pipeline/workflows.py` 中替换为 Scanpy/scvi-tools/Squidpy
- R：在 `R/scripts/run_r_pipeline.R` 中替换为 Seurat/Signac 工作流

## 5) 每次分析记录（强烈建议）
每次关键分析都更新 `docs/analysis-log.md`：
- 改了什么参数
- 发现了什么现象
- 下一步做什么

## 6) 运行第一个教学脚本（Stereo-seq: LC_4B）
```bash
python python/scripts/01_data_loading_and_qc.py
```

脚本会输出：
- `data/results/LC_4B/01_qc/qc_metrics_before_after.csv`
- `data/results/LC_4B/01_qc/qc_violin_before_after.png`
- `data/results/LC_4B/01_qc/kept_bins_index.csv`
