# Methodology

## 1. Why we classify by modality (and why it's not in the data)

Public pharma financials report revenue by **product** (Keytruda, Ozempic), **therapeutic area** (Oncology, Immunology), or **geography** — never by modality. This project constructs a modality view by mapping every material product to one of six buckets, then aggregating revenue up to company level.

## 2. Modality definitions

We use six mutually exclusive buckets. A product is assigned to **exactly one** bucket using the first matching rule.

| Modality | Definition | Examples |
|---|---|---|
| **mRNA** | Lipid-nanoparticle-delivered messenger RNA | Comirnaty, Spikevax |
| **Vaccine (non-mRNA)** | Subunit, conjugate, live-attenuated, viral vector | Prevnar, Shingrix, Gardasil |
| **ADC** | Antibody-drug conjugate (mAb + cytotoxic payload via linker) | Enhertu, Padcev, Kadcyla |
| **Cell & gene therapy** | Autologous/allogeneic cell products and in-vivo gene therapy | Yescarta, Kymriah, Zolgensma, Hemgenix |
| **Biologic (other)** | Monoclonal antibodies, peptides, fusion proteins, recombinant proteins. Listed in FDA Purple Book and not in any bucket above. | Humira, Keytruda, Ozempic, Dupixent |
| **Small molecule** | Chemically synthesized; default bucket | Eliquis, Trikafta, Tagrisso, Jardiance |

### Classification rules (apply in order)

1. If the product is an mRNA vaccine → **mRNA**
2. If the product is in CDC ACIP vaccine schedule and not mRNA → **Vaccine (non-mRNA)**
3. If the product label describes an antibody-drug conjugate or has "-tuzumab vedotin / deruxtecan / govitecan / emtansine" stem → **ADC**
4. If the product is a cell therapy (CAR-T, TCR-T, NK) or in-vivo AAV/LNP gene therapy → **Cell & gene therapy**
5. If the product is listed in the FDA Purple Book (any other biologic) → **Biologic (other)**
6. Otherwise → **Small molecule**

### Edge cases and how we handle them

| Case | Decision | Rationale |
|---|---|---|
| GLP-1 peptides (Ozempic, Mounjaro) | Biologic (other) | Synthesized as peptide; behaves commercially like a biologic |
| Biosimilars | Same modality as originator | Modality is the molecule, not the brand |
| Combination products (e.g., Biktarvy: 3 small molecules) | Small molecule | All components share modality |
| Oligonucleotides (siRNA, antisense — e.g., Leqvio, Spinraza) | Biologic (other) | Not small molecule; not LNP-mRNA |
| Radioligand therapy (Pluvicto) | Biologic (other) | Mark with a flag for potential future split |

All edge-case decisions are logged in `data/modality_classification.csv` with a `notes` column.

## 3. Company universe — top 20 selection

Selected by **average market cap across the 2024 calendar year** (4 quarter-end snapshots from yfinance). This avoids snapshot bias from a single date. Re-ranked annually; the universe is held constant for the analysis window to keep year-over-year comparisons clean.

## 4. Revenue scope

- **Source:** Company-reported segment and product-level disclosures in 10-K, 20-F, or equivalent annual report.
- **Currency:** All revenue converted to USD at the company's reporting-year average rate (disclosed in the annual report). Avoids period-end FX distortions.
- **Coverage:** Products with ≥$500M annual sales are individually classified. Products below this threshold are bucketed into "Other [modality]" using the company's segment disclosure as a proxy.
- **Inclusions:** Net product sales only. Excludes royalties, collaboration revenue, and contract manufacturing (CDMO) revenue where separately reported.

## 5. Metrics

- **Revenue CAGR (2020–2024):** `(rev_2024 / rev_2020) ^ (1/4) - 1`. For modalities not present in 2020 (mRNA), computed from first year of meaningful revenue with the start year flagged.
- **Modality share:** Modality revenue ÷ total top-20 revenue, by year.
- **Concentration (HHI):** Herfindahl-Hirschman Index per modality per year. HHI = Σ(share_i)² × 10,000, where share_i is each company's share of that modality's top-20 revenue.
- **Share shift:** Percentage-point change in modality share between 2020 and 2024.

## 6. Known limitations

- Product-level granularity below $500M is approximated.
- Private companies (Boehringer Ingelheim) and JV revenue (Comirnaty Pfizer/BioNTech split) require disclosure-based estimates.
- Modality assignment for combination/multi-modality assets is single-bucketed; a sensitivity check is provided in the notebook.
- Annual report fiscal years differ; we align to calendar year using the closest reporting period.

## 7. Reproducibility

Every raw download is timestamped under `data/raw/{source}/{date}/`. Classification CSV is version-controlled. Analysis runs end-to-end from `make all` or the notebook sequence 01 → 04.
