"""
SEC EDGAR quickstart: pull annual revenue for one US-listed biopharma.

Run this first to confirm:
1. Your environment has requests + pandas installed
2. The SEC EDGAR API responds to your User-Agent
3. You can extract Revenues XBRL facts from companyfacts.json

Once this works, ask Claude Code to:
  "Generalize this script to loop over every row in data/company_universe.csv
   where reports_in_sec == 'Yes', save annual revenue 2018-2024 to
   data/raw/sec_edgar/{ticker}_revenue.csv"

Usage:
  python src/sec_edgar_quickstart.py
"""

import time
from pathlib import Path

import pandas as pd
import requests

# SEC requires a descriptive User-Agent identifying you. Replace with your info.
HEADERS = {
    "User-Agent": "Your Name your.email@example.com",
    "Accept-Encoding": "gzip, deflate",
}

# Pfizer's CIK (10-digit, zero-padded)
TICKER = "PFE"
CIK = "0000078003"

# SEC enforces 10 requests/second. We sleep to stay well under.
RATE_LIMIT_SLEEP = 0.15


def fetch_company_facts(cik: str) -> dict:
    """Get all XBRL-tagged financial facts for a company."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    time.sleep(RATE_LIMIT_SLEEP)
    return response.json()


def extract_annual_revenue(facts: dict) -> pd.DataFrame:
    """
    Pull annual revenue from the us-gaap taxonomy.

    Companies tag revenue differently. We try common concepts in order
    and use the first one that returns data.
    """
    candidates = [
        "Revenues",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "SalesRevenueNet",
    ]

    us_gaap = facts.get("facts", {}).get("us-gaap", {})

    for concept in candidates:
        if concept in us_gaap:
            usd_facts = us_gaap[concept].get("units", {}).get("USD", [])
            if not usd_facts:
                continue

            df = pd.DataFrame(usd_facts)
            # Keep only 10-K filings (annual), full fiscal year (~365 days)
            df["start"] = pd.to_datetime(df["start"])
            df["end"] = pd.to_datetime(df["end"])
            df["days"] = (df["end"] - df["start"]).dt.days

            annual = df[
                (df["form"] == "10-K")
                & (df["days"].between(350, 380))
                & (df["fp"] == "FY")
            ].copy()

            if annual.empty:
                continue

            annual["fiscal_year"] = annual["end"].dt.year
            # Deduplicate (sometimes restated); keep the latest filing
            annual = (
                annual.sort_values("filed", ascending=False)
                .drop_duplicates("fiscal_year")
                .sort_values("fiscal_year")
            )

            result = annual[["fiscal_year", "val", "form", "filed"]].rename(
                columns={"val": "revenue_usd"}
            )
            result["concept_used"] = concept
            return result.reset_index(drop=True)

    raise RuntimeError("No revenue concept found in company facts.")


def main() -> None:
    print(f"Fetching SEC EDGAR data for {TICKER} (CIK {CIK})...")

    if HEADERS["User-Agent"].startswith("Your Name"):
        print("\n⚠️  Edit HEADERS at the top of this file with your real name + email.")
        print("    SEC blocks requests with a generic User-Agent.\n")
        return

    facts = fetch_company_facts(CIK)
    print(f"  Entity: {facts.get('entityName')}")

    revenue = extract_annual_revenue(facts)
    revenue["revenue_usd_bn"] = (revenue["revenue_usd"] / 1e9).round(2)

    print(f"\nAnnual revenue for {TICKER}:")
    print(revenue[["fiscal_year", "revenue_usd_bn", "concept_used"]].to_string(index=False))

    # Save raw output
    out_dir = Path("data/raw/sec_edgar")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{TICKER}_revenue.csv"
    revenue.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
