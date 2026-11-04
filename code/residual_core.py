"""
residual_core.py — Human-readable residual primitives for language-circuit.

Three residual operations used throughout the work:
1. residual_ranking: inverse-PageRank-style ranking by residual validity CV_G = exp(-R_G)
2. trajectory_quantize: edge extraction of discrete quanta from a continuous residual trajectory
3. ENCORE-style residual acceleration: dual residual |DUT - ref| and validity contraction

Run with: python residual_core.py
All functions preserve the residual contract and edge-extraction semantics.
"""

import numpy as np

def residual_ranking(candidates, residuals):
    """Inverse PageRank style residual ranking with validity CV_G = exp(-R_G)."""
    validity = np.exp(-np.array(residuals))
    order = np.argsort(-validity)
    return {
        'candidates': candidates,
        'residuals': residuals,
        'validity': np.round(validity, 4).tolist(),
        'ranked': [candidates[i] for i in order]
    }

def trajectory_quantize(continuum, levels):
    """Edge extraction: snap continuous residual trajectory to discrete quanta by nearest residual level."""
    quantized = levels[np.argmin(np.abs(continuum[:, None] - levels), axis=1)]
    return quantized, np.unique(quantized)

if __name__ == "__main__":
    # Round 1: residual ranking
    cands = ['the', 'quick', 'brown', 'fox', 'jumps']
    res = [0.1, 0.8, 0.3, 0.5, 1.2]
    print("=== Residual Ranking ===")
    print(residual_ranking(cands, res))

    # Round 2: trajectory quantization (edge sampling)
    t = np.linspace(0, 10, 100)
    cont = 5 * np.sin(t) + 2 * np.sin(3*t)
    lvls = np.linspace(-7, 7, 5)
    q, uniq = trajectory_quantize(cont, lvls)
    print("\n=== Trajectory Quantization ===")
    print("Sample continuum:", np.round(cont[:5], 2))
    print("Quantized:", q[:5])
    print("Unique quanta:", uniq)

    # Round 3: ENCORE-style residual acceleration
    dut = cont + 0.01 * np.random.randn(len(cont))
    residual = np.abs(dut - cont)
    validity = np.exp(-residual * 10)
    print("\n=== ENCORE Residual Acceleration ===")
    print("Mean residual:", np.round(np.mean(residual), 4))
    print("Mean validity:", np.round(np.mean(validity), 4))
