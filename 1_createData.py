import numpy as np
import pandas as pd

def simulate_and_save_data(
    p_aug=0.10,
    p_sep_A=0.10,
    uplift=0.02,
    n_aug=1000,
    n_sep_A=500,
    n_sep_B=500,
    seed=7,
    filename="conversion_data_2025_08_09.csv"
):
    rng = np.random.default_rng(seed)
    p_sep_B = min(max(p_sep_A + uplift, 0.0), 1.0)

    # 2025-08 baseline
    df_aug = pd.DataFrame({
        "month": "2025-08",
        "group": "baseline",
        "y": rng.binomial(1, p_aug, size=n_aug)
    })

    # 2025-09 A/B experiment
    df_sep = pd.DataFrame({
        "month": "2025-09",
        "group": ["A"] * n_sep_A + ["B"] * n_sep_B,
        "y": np.concatenate([
            rng.binomial(1, p_sep_A, size=n_sep_A),
            rng.binomial(1, p_sep_B, size=n_sep_B)
        ])
    })

    df = pd.concat([df_aug, df_sep], ignore_index=True)
    df.to_csv(filename, index=False)

    return df

# 실행
df = simulate_and_save_data(
    p_aug=0.10,
    p_sep_A=0.10,
    uplift=0.02,
    filename="conversion_data_2025_08_09.csv"
)

print("Saved file: conversion_data_2025_08_09.csv")
print(df.groupby(["month", "group"])["y"].agg(["count", "sum", "mean"]))
