# Top 20 Biopharma — Revenue & Market Cap by Modality (2020–2024)

> A market-insight analysis of where commercial value is shifting across the global biopharma industry, by therapeutic modality.

## The questions this project answers

1. **Growth** — Which modalities (small molecule, biologic, ADC, mRNA, vaccine, cell & gene) are growing fastest by revenue CAGR 2020–2024?
2. **Concentration** — Which modalities are winner-take-most markets vs. fragmented? (HHI index)
3. **Positioning** — Which top-20 companies are most exposed to growing modalities, and which are concentrated in declining ones?
4. **Valuation gap** — Where does market cap diverge most from current revenue, and what does that say about investor expectations on modality bets?

## Why this matters (sales / commercial lens)

- Sales effort is finite. Knowing which modality buckets are growing 3x faster than industry average tells BD teams where to focus partnership and licensing efforts.
- Companies over-indexed on declining modalities (e.g., biosimilar-eroded biologics, post-COVID vaccines) face revenue cliffs that change competitive dynamics.
- White-space modalities with few top-20 players (ADC, cell & gene) signal where smaller biotechs can carve commercial niches.

## Headline findings (fill in after analysis)

- _Finding 1:_ ...
- _Finding 2:_ ...
- _Finding 3:_ ...

## Methodology

See [`docs/methodology.md`](docs/methodology.md). Key choice: revenue-by-modality is not directly reported by companies, so this project builds it by classifying every product (>$500M annual sales) from each top-20 company's annual report into one of six modality buckets, then aggregating.

## Data sources (all free)

| Source | Use | Access |
|---|---|---|
| SEC EDGAR XBRL API | Total revenue, US-listed top-20 | Free, no API key, 10 req/sec |
| Company annual report PDFs | Product-level revenue (all 20) | Investor relations sites |
| yfinance | Market cap time series | Free Python library |
| FDA Purple Book | Biologic classification check | Free download |
| FDA Orange Book | Small molecule check | Free download |
| ClinicalTrials.gov API | Pipeline modality cross-check | Free, no key |
| IQVIA Institute reports | Industry-level sanity checks | Free PDFs |

## Repo structure

```
data/
  company_universe.csv               # the 20 companies
  modality_classification.csv        # drug → modality mapping
  raw/                               # untouched downloads
  processed/                         # final analysis-ready tables
docs/
  methodology.md                     # how modalities are defined and classified
src/
  ingest/                            # SEC EDGAR, yfinance, PDF parsers
  classify/                          # modality assignment logic
  transform/                         # aggregation, normalization
  analyze/                           # CAGR, HHI, share-shift
notebooks/                           # exploration + chart drafts
dashboard/                           # Streamlit app
```

## Tech stack

Python 3.11, pandas, requests, yfinance, pdfplumber, plotly, streamlit.

## How to reproduce

```bash
pip install -r requirements.txt
python src/sec_edgar_quickstart.py    # confirms API access
# (then run remaining pipeline scripts in order)
streamlit run dashboard/app.py
```

## Author

Yoonji Lee — Pharmaceutical sales specialist building data analytics skills through hands-on portfolio projects * Coworked with AI
