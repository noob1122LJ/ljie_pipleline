#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 运行前建议（按需创建虚拟环境后执行）：
# pip install stereopy pandas numpy scipy matplotlib seaborn

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import stereo as st
from scipy import sparse

# ==============================
# 0. 参数区（初学阶段建议只改这里）
# ==============================
gef_file = "data/raw/LC_4B.bm.gef"   # 你的 Stereo-seq 输入文件
bin_size = 50                         # 题目要求：Bin 50
sample_id = "LC_4B"
output_dir = "data/results/LC_4B/01_qc"
os.makedirs(output_dir, exist_ok=True)

# 常见的基础过滤阈值（教学示例，可在后续按数据分布调整）
min_genes_per_bin = 150
max_mito_pct = 20.0

print("=" * 80)
print("[01] Stereo-seq 数据读取 + 基础质控开始")
print(f"输入文件: {gef_file}")
print(f"Bin size: {bin_size}")
print("=" * 80)

# ==============================
# 1. 读取 Stereo-seq GEF（Bin 50）
# ==============================
# 为什么空转数据常按 Bin 分析？
# - 原始坐标级别信号很稀疏，直接逐点分析会有大量零计数。
# - 按 Bin（例如 50x50）聚合后，可提高信号稳定性，降低噪声。
# - Bin 是空间分辨率与统计稳定性的折中：Bin 越小，空间分辨率高但更稀疏；
#   Bin 越大，信号更稳定但空间细节会损失。

data = st.io.read_gef(
    file_path=gef_file,
    bin_type="bins",
    bin_size=bin_size,
)

print("[INFO] 数据读取完成。")
print(f"[INFO] Bin 数量（spots/bins）: {data.n_cells}")
print(f"[INFO] 基因数量（features）: {data.n_genes}")

# ==============================
# 2. 计算每个 Bin 的 QC 指标
# ==============================
# MID 是什么？
# - MID = Molecular Identifier（分子标识计数）。
# - 在空间转录组中，一个 Bin 的总 MID 可近似理解为该位置捕获到的总转录本分子量。
# - MID 越低，通常信号越弱，可能代表背景区域或低质量点。

# exp_matrix 一般是稀疏矩阵（节省内存），这里转成 CSR 便于行列求和
exp_matrix = data.exp_matrix
if not sparse.issparse(exp_matrix):
    exp_matrix = sparse.csr_matrix(exp_matrix)
else:
    exp_matrix = exp_matrix.tocsr()

# 每个 Bin 的总 MID（按行求和）
total_mid = np.array(exp_matrix.sum(axis=1)).reshape(-1)

# 每个 Bin 检测到的基因数（非零基因个数）
# 为什么过滤低基因数 Bin？
# - 低基因数通常意味着信号很弱、技术噪声占比高。
# - 保留过多低基因数 Bin 会干扰聚类、注释和差异分析，导致结果不稳定。
# - 所以先做最低限度过滤，可提升后续分析的可信度。
n_genes_by_bin = np.array((exp_matrix > 0).sum(axis=1)).reshape(-1)

# 提取基因名（兼容 stereopy 常见字段）
if hasattr(data.genes, "gene_name"):
    gene_names = np.array(data.genes.gene_name)
elif hasattr(data.genes, "index"):
    gene_names = np.array(data.genes.index)
else:
    gene_names = np.array(data.genes)

# 识别线粒体基因（人类常见前缀 MT-；也兼容小写 mt-）
mito_mask = np.char.startswith(gene_names.astype(str), "MT-") | np.char.startswith(gene_names.astype(str), "mt-")

if mito_mask.sum() == 0:
    print("[WARN] 没有识别到线粒体基因（MT-/mt-）。mito_pct 将记为 0。")
    mito_mid = np.zeros_like(total_mid)
else:
    mito_mid = np.array(exp_matrix[:, mito_mask].sum(axis=1)).reshape(-1)

mito_pct = np.where(total_mid > 0, mito_mid / total_mid * 100, 0.0)

qc_before = pd.DataFrame(
    {
        "sample_id": sample_id,
        "total_mid": total_mid,
        "n_genes_by_bin": n_genes_by_bin,
        "mito_pct": mito_pct,
        "status": "before_qc",
    }
)

print("[INFO] QC 指标计算完成（过滤前）。")
print(qc_before[["total_mid", "n_genes_by_bin", "mito_pct"]].describe())

# ==============================
# 3. 按阈值过滤低质量 Bin
# ==============================
keep_mask = (qc_before["n_genes_by_bin"] >= min_genes_per_bin) & (qc_before["mito_pct"] <= max_mito_pct)

print(f"[INFO] 过滤阈值: n_genes_by_bin >= {min_genes_per_bin}, mito_pct <= {max_mito_pct}")
print(f"[INFO] 过滤前 Bin 数: {qc_before.shape[0]}")
print(f"[INFO] 保留 Bin 数: {keep_mask.sum()}")
print(f"[INFO] 过滤掉 Bin 数: {(~keep_mask).sum()}")

# 过滤后的矩阵（保留高质量 Bin）
exp_matrix_after = exp_matrix[keep_mask.values, :]

total_mid_after = np.array(exp_matrix_after.sum(axis=1)).reshape(-1)
n_genes_by_bin_after = np.array((exp_matrix_after > 0).sum(axis=1)).reshape(-1)

if mito_mask.sum() == 0:
    mito_mid_after = np.zeros_like(total_mid_after)
else:
    mito_mid_after = np.array(exp_matrix_after[:, mito_mask].sum(axis=1)).reshape(-1)

mito_pct_after = np.where(total_mid_after > 0, mito_mid_after / total_mid_after * 100, 0.0)

qc_after = pd.DataFrame(
    {
        "sample_id": sample_id,
        "total_mid": total_mid_after,
        "n_genes_by_bin": n_genes_by_bin_after,
        "mito_pct": mito_pct_after,
        "status": "after_qc",
    }
)

# ==============================
# 4. 质控前后小提琴图对比并保存
# ==============================
qc_all = pd.concat([qc_before, qc_after], axis=0, ignore_index=True)
qc_all.to_csv(f"{output_dir}/qc_metrics_before_after.csv", index=False)

sns.set(style="whitegrid", font_scale=1.1)
fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

sns.violinplot(data=qc_all, x="status", y="total_mid", ax=axes[0], cut=0)
axes[0].set_title("Total MID")
axes[0].set_xlabel("")

sns.violinplot(data=qc_all, x="status", y="n_genes_by_bin", ax=axes[1], cut=0)
axes[1].set_title("Detected Genes per Bin")
axes[1].set_xlabel("")

sns.violinplot(data=qc_all, x="status", y="mito_pct", ax=axes[2], cut=0)
axes[2].set_title("Mitochondrial Ratio (%)")
axes[2].set_xlabel("")

plt.tight_layout()
fig_path = f"{output_dir}/qc_violin_before_after.png"
plt.savefig(fig_path, dpi=300)
plt.close()

# 额外保存过滤后 Bin 的索引和名称（方便后续步骤继续用）
filtered_bin_index = np.where(keep_mask.values)[0]
pd.DataFrame({"bin_index": filtered_bin_index}).to_csv(
    f"{output_dir}/kept_bins_index.csv", index=False
)

if hasattr(data.cells, "cell_name"):
    kept_bin_names = np.array(data.cells.cell_name)[keep_mask.values]
    pd.DataFrame({"bin_name": kept_bin_names}).to_csv(
        f"{output_dir}/kept_bins_name.csv", index=False
    )

print("=" * 80)
print("[DONE] 01_data_loading_and_qc.py 执行完成")
print(f"[OUT] QC 指标表: {output_dir}/qc_metrics_before_after.csv")
print(f"[OUT] 小提琴图: {fig_path}")
print(f"[OUT] 保留 Bin 索引: {output_dir}/kept_bins_index.csv")
print("=" * 80)
