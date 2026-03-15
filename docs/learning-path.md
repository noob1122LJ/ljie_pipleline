# 学习路径建议（面向单细胞/多组学/空间组学）

## 第 1 阶段：理解数据与任务
1. 明确每种模态的输入文件格式（10x、h5ad、loom、Visium 等）。
2. 确定每个样本的元信息（组织、批次、条件）。
3. 先定义好输出物：
   - QC 报告
   - 细胞注释
   - 差异分析
   - 空间可视化图

## 第 2 阶段：打通最小闭环
1. 从一个样本起步。
2. 完成：读入 -> QC -> 降维聚类 -> marker -> 可视化。
3. 把参数沉淀到 `configs/project.yaml`，保证复现。

## 第 3 阶段：走向多样本与多组学整合
1. 加入批次校正。
2. 尝试跨模态对齐（如 RNA + ATAC）。
3. 空间组学中补充邻域分析和细胞通讯分析。

## 推荐工具（按语言）
- Python: Scanpy, scvi-tools, Muon, Squidpy
- R: Seurat, Signac, SingleR, CellChat, Giotto
