#!/usr/bin/env python3
"""
Financial Statement Analyzer
- Reads a CSV with financial line items by period
- Computes common ratios
- Exports an Excel report and PNG charts
"""

import argparse
import os
import sys
from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

REQUIRED_COLUMNS = [
    "period",
    "revenue",
    "cogs",
    "operating_income",
    "net_income",
    "total_assets",
    "total_equity",
    "total_liabilities",
    "current_assets",
    "current_liabilities",
    "cash",
    "marketable_securities",
    "accounts_receivable",
    "inventory",
    "interest_expense",
]

def validate_columns(df: pd.DataFrame) -> List[str]:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing

def compute_ratios(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    eps = 1e-9

    # Margins
    out["gross_profit"] = out["revenue"] - out["cogs"]
    out["gross_margin"] = out["gross_profit"] / (out["revenue"] + eps)
    out["operating_margin"] = out["operating_income"] / (out["revenue"] + eps)
    out["net_margin"] = out["net_income"] / (out["revenue"] + eps)

    # Liquidity
    out["current_ratio"] = out["current_assets"] / (out["current_liabilities"] + eps)
    quick_assets = out["cash"] + out["marketable_securities"] + out["accounts_receivable"]
    out["quick_ratio"] = quick_assets / (out["current_liabilities"] + eps)

    # Leverage
    out["debt_to_equity"] = out["total_liabilities"] / (out["total_equity"] + eps)

    # Efficiency
    out["asset_turnover"] = out["revenue"] / (out["total_assets"] + eps)

    # Profitability
    out["roa"] = out["net_income"] / (out["total_assets"] + eps)
    out["roe"] = out["net_income"] / (out["total_equity"] + eps)

    # Coverage
    out["interest_coverage"] = out["operating_income"] / (out["interest_expense"] + eps)

    # Growth (YoY) — compute percentage change by sorted period
    out = out.sort_values("period").reset_index(drop=True)
    out["revenue_growth_yoy"] = out["revenue"].pct_change()
    out["net_income_growth_yoy"] = out["net_income"].pct_change()

    ratio_cols = [
        "period",
        "gross_margin",
        "operating_margin",
        "net_margin",
        "current_ratio",
        "quick_ratio",
        "debt_to_equity",
        "asset_turnover",
        "roa",
        "roe",
        "interest_coverage",
        "revenue_growth_yoy",
        "net_income_growth_yoy",
    ]
    return out[ratio_cols]

def export_excel(raw_df: pd.DataFrame, ratios_df: pd.DataFrame, out_path: str) -> None:
    import openpyxl  # noqa: F401
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        raw_df.to_excel(writer, sheet_name="Raw Data", index=False)
        ratios_df.to_excel(writer, sheet_name="Ratios", index=False)

def plot_margins(ratios: pd.DataFrame, out_path: str) -> None:
    plt.figure()
    for col in ["gross_margin", "operating_margin", "net_margin"]:
        plt.plot(ratios["period"], ratios[col], marker="o", label=col.replace("_", " ").title())
    plt.title("Margins by Period")
    plt.xlabel("Period")
    plt.ylabel("Ratio")
    plt.legend()
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

def plot_roa_roe(ratios: pd.DataFrame, out_path: str) -> None:
    plt.figure()
    for col in ["roa", "roe"]:
        plt.plot(ratios["period"], ratios[col], marker="o", label=col.upper())
    plt.title("ROA and ROE by Period")
    plt.xlabel("Period")
    plt.ylabel("Ratio")
    plt.legend()
    plt.savefig(out_path, bbox_inches="tight")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Financial Statement Analyzer")
    parser.add_argument("--input", required=True, help="Path to input CSV containing financial data")
    parser.add_argument("--outdir", default="./out", help="Directory to save outputs (default: ./out)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.input)
    missing = validate_columns(df)
    if missing:
        print("ERROR: Missing required columns:", ", ".join(missing), file=sys.stderr)
        sys.exit(2)

    ratios = compute_ratios(df)

    excel_path = os.path.join(args.outdir, "financial_report.xlsx")
    export_excel(df, ratios, excel_path)

    margins_png = os.path.join(args.outdir, "margins_by_period.png")
    roa_roe_png = os.path.join(args.outdir, "roa_roe_by_period.png")
    plot_margins(ratios, margins_png)
    plot_roa_roe(ratios, roa_roe_png)

    print(" Done.")
    print(f"Excel report: {excel_path}")
    print(f"Margins chart: {margins_png}")
    print(f"ROA/ROE chart: {roa_roe_png}")

if __name__ == "__main__":
    main()
