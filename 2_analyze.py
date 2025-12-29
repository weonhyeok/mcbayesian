import numpy as np
import pandas as pd

def make_beta_prior_from_aug(y_aug, prior_strength=200, base_a=1.0, base_b=1.0):
    """
    8월 데이터를 이용해 Beta prior 구성
    prior_strength = pseudo-sample size
    """
    n = y_aug.size
    s = int(y_aug.sum())
    p_hat = s / n

    a = base_a + prior_strength * p_hat
    b = base_b + prior_strength * (1 - p_hat)
    return a, b, p_hat


def bayesian_ab_from_csv(
    filename="conversion_data_2025_08_09.csv",
    prior_strength=200,
    draws=200_000,
    seed=1
):
    rng = np.random.default_rng(seed)
    df = pd.read_csv(filename)

    # split data
    y_aug = df.loc[df["month"] == "2025-08", "y"].to_numpy()
    y_A = df.loc[(df["month"] == "2025-09") & (df["group"] == "A"), "y"].to_numpy()
    y_B = df.loc[(df["month"] == "2025-09") & (df["group"] == "B"), "y"].to_numpy()

    # prior from August
    a0, b0, p_aug_hat = make_beta_prior_from_aug(y_aug, prior_strength)

    # posterior parameters
    sA, nA = int(y_A.sum()), y_A.size
    sB, nB = int(y_B.sum()), y_B.size

    aA, bA = a0 + sA, b0 + (nA - sA)
    aB, bB = a0 + sB, b0 + (nB - sB)

    # draw posterior samples
    pA = rng.beta(aA, bA, size=draws)
    pB = rng.beta(aB, bB, size=draws)

    diff = pB - pA

    return {
        "aug_empirical_rate": p_aug_hat,
        "prior_beta": (a0, b0),
        "sep_counts": {
            "A": {"success": sA, "n": nA},
            "B": {"success": sB, "n": nB}
        },
        "posterior_mean_A": float(pA.mean()),
        "posterior_mean_B": float(pB.mean()),
        "P(B > A | data)": float((diff > 0).mean()),
        "uplift_mean": float(diff.mean()),
        "uplift_95_CI": tuple(np.quantile(diff, [0.025, 0.975])),
    }

# 실행
result = bayesian_ab_from_csv(
    filename="conversion_data_2025_08_09.csv",
    prior_strength=200
)

for k, v in result.items():
    print(f"{k}: {v}")
