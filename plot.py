#!/usr/bin/env python
"""Post-process results from a 2x2 VAWT actuator line simulation in OpenFOAM."""

import pandas as pd
import matplotlib.pyplot as plt
import os

try:
    import seaborn
except ImportError:
    plt.style.use("ggplot")

def plot_cp(angle0=540.0):
    base_path = "postProcessing/turbines/0"
    turbine_files = ["turbine1.csv", "turbine2.csv", "turbine3.csv", "turbine4.csv"]

    plt.figure(figsize=(10, 6))

    for i, fname in enumerate(turbine_files, start=1):
        path = os.path.join(base_path, fname)
        if not os.path.isfile(path):
            print(f"⚠️ File not found: {path}")
            continue

        df = pd.read_csv(path)
        df = df.drop_duplicates("time", keep="last")

        if df.angle_deg.max() < angle0:
            angle0 = 0.0

        print(f"\nTurbine {i} performance from {angle0:.1f}–{df.angle_deg.max():.1f} degrees:")
        print(f"Mean TSR = {df.tsr[df.angle_deg >= angle0].mean():.2f}")
        print(f"Mean C_P = {df.cp[df.angle_deg >= angle0].mean():.2f}")
        print(f"Mean C_D = {df.cd[df.angle_deg >= angle0].mean():.2f}")

        plt.plot(df.angle_deg, df.cp, label=f"Turbine {i}")

    plt.xlabel("Azimuthal angle (degrees)")
    plt.ylabel("$C_P$")
    plt.title("Power Coefficient vs Azimuthal Angle for 2×2 VAWT Array")
    plt.legend()
    plt.tight_layout()

if __name__ == "__main__":
    plot_cp()
    plt.show()
