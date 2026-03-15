#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript R/scripts/run_r_pipeline.R <config.yaml>")
}

config_path <- args[[1]]
if (!requireNamespace("yaml", quietly = TRUE)) {
  stop("Please install package: yaml")
}

cfg <- yaml::read_yaml(config_path)
project_name <- cfg$project$name
samples <- cfg$samples

processed_dir <- cfg$io$processed_dir
results_dir <- cfg$io$results_dir

if (!dir.exists(processed_dir)) dir.create(processed_dir, recursive = TRUE)
if (!dir.exists(results_dir)) dir.create(results_dir, recursive = TRUE)

cat(sprintf("[R] Project: %s\n", project_name))
cat(sprintf("[R] Samples loaded: %d\n", length(samples)))
cat("[R] TODO: Replace template with Seurat/Signac/Spatial workflow.\n")
