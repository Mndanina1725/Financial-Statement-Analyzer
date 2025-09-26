# Financial Statement Analyzer (CS + Econ Portfolio Project)

This project reads a CSV of basic financial statement line items (by period), computes key financial ratios,
and produces a polished Excel report and charts suitable for a resume/portfolio.

## What it does
- Loads financial statement data from CSV (e.g., yearly or quarterly).
- Computes 12+ common ratios: margins (gross/operating/net), liquidity (current/quick), leverage (D/E),
  efficiency (asset turnover), profitability (ROA/ROE), coverage (interest coverage), and YoY growth.
- Exports an Excel workbook with **Raw Data** and **Ratios** sheets.
- Saves two PNG charts: **margins_by_period.png** and **roa_roe_by_period.png**.

## Install
```bash
pip install -r requirements.txt
```

## Run
```bash
python analyzer.py --input sample_financials.csv --outdir ./out
```
- `--input`: path to your CSV
- `--outdir`: output directory (created if missing)

## CSV Format
Provide one row per period (year or quarter). Required columns (case-sensitive):  
`period,revenue,cogs,operating_income,net_income,total_assets,total_equity,total_liabilities,current_assets,current_liabilities,cash,marketable_securities,accounts_receivable,inventory,interest_expense`

See `sample_financials.csv` for an example.

## Example
```bash
python analyzer.py --input sample_financials.csv --outdir ./out
```
Outputs:
- `out/financial_report.xlsx`
- `out/margins_by_period.png`
- `out/roa_roe_by_period.png`
```

## Notes
- `operating_income` is used as a proxy for EBIT to compute interest coverage.
- Add more ratios/features as needed; this is designed to be extended.
