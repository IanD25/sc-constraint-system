# Project Log — Supply Chain Constraint System

## Pilot Study: Automotive Tier 1 Suppliers

---

## Phase 0: Environment Setup & Data Infrastructure

### Date: March 2, 2026

### 0.1 Development Environment

**Decision:** VS Code + Terminal on macOS, Python virtual environment, GitHub for version control.

**Setup completed:**
- Python 3.13 (system install on macOS)
- Virtual environment at `~/Projects/sc-constraint-system/.venv`
- Git initialized, remote set to `github.com/IanD25/sc-constraint-system` (private repo)
- Dependencies installed via `requirements.txt`:
  - simfin, pandas, numpy, python-dotenv
  - networkx, statsmodels, scikit-learn, scipy
  - matplotlib, seaborn, requests, beautifulsoup4, lxml, jupyter

**Technical issue resolved:** SimFin's `sf.load()` function is incompatible with Python 3.13 + pandas 3.x (deprecated `date_parser` argument in `pd.read_csv()`). Workaround: bypass `sf.load()` entirely — use SimFin only to trigger bulk CSV downloads, then read the CSVs directly with modern pandas. This workaround is implemented in all pipeline scripts.

**Technical issue resolved:** GitHub no longer accepts password authentication for git push. Solution: Personal Access Token embedded in remote URL.

**Folder structure:**
```
sc-constraint-system/
├── data/
│   ├── raw/simfin/          # SimFin bulk CSVs (gitignored)
│   ├── raw/sec_edgar/       # SEC filings (future)
│   ├── raw/fred/            # FRED macro data (future)
│   ├── processed/           # Pipeline output CSVs
│   └── final/               # Analysis-ready datasets
├── src/
│   └── data_collection/
│       ├── simfin_pipeline.py      # v1 — original 10-ticker (broken sf.load)
│       ├── simfin_pipeline_v3.py   # v3 — expanded 52-ticker sample
│       └── simfin_discovery.py     # Universe scan script
├── analysis/                # Phase-specific analysis notebooks (future)
├── docs/                    # Paper, consultancy, taxonomy docs
├── output/                  # Figures, tables, reports
├── config/                  # Configuration files
├── .env                     # API keys (gitignored)
├── .gitignore
└── requirements.txt
```

### 0.2 SimFin Data Connection

**Data source:** SimFin free tier (bulk CSV download, quarterly financial statements for US market).

**API key:** Stored in `.env` file (gitignored). Free tier provides quarterly income, balance sheet, and cash flow statements for ~6,500 US companies.

**Data format:** Semicolon-delimited CSVs with columns including Ticker, Report Date, Revenue, Cost of Revenue, Gross Profit, etc.

---

### 0.3 Initial Pilot — 10 Tickers

**Date:** March 2, 2026

**Script:** `simfin_pipeline.py` (v2 — direct CSV reading)

**Ticker selection rationale:** 5 paired comparisons testing specific framework dimensions:

| Pair | Ticker A | Ticker B | Dimension Tested |
|------|----------|----------|-----------------|
| Drivetrain | AXL (extreme GM dependency) | DAN (diversified customers) | D1 Network Position |
| Seating | ADNT (pure-play) | LEA (multi-segment) | D4 Stack Architecture |
| Thermal | MOD (data center pivot) | THRM (higher IP) | D2 Information Asymmetry |
| Electronics | VC (cockpit, higher tech) | SRI (sensors, smaller) | D3 Elasticity |
| P/C boundary | GNTX (IP/product moat) | APTV (systems arch moat) | Margin Mode boundary |

**Outcome:**
- 8 of 10 tickers found in SimFin (ADNT and MOD missing from free dataset)
- 152 rows retrieved (19 quarters each, Q4 2020 – Q4 2024)
- Pipeline successfully constructed margin, balance sheet, cash flow, and rolling metric variables
- Data quality: ~15% null rate on some columns (R&D expense, SGA) — expected for firms that don't break out these line items

**Issue identified:** "Accounts Payable" column name mismatch — SimFin uses "Payables & Accruals" instead. Handled by `safe_col()` fallback function in v3.

---

### 0.4 Universe Discovery Scan

**Date:** March 2, 2026

**Script:** `simfin_discovery.py`

**Purpose:** Determine realistic sample size for the pilot study by scanning the full SimFin US universe for automotive-related companies.

**Results:**
- SimFin US universe: 6,526 companies total
- Companies with quarterly income data: 3,636
- Full 19-quarter panel (Q4 2020 – Q4 2024): 1,690 tickers
- Auto-related by industry classification: 208 companies
- Known auto tickers found (from curated list of 78): 56

**22 known auto tickers NOT found:** ADNT, MOD, BWA, ALV, MGA, HON, HUN, PHIN, PPG, SNA, TXT, and others. These are either not in SimFin's free tier, have been acquired/delisted, or use different ticker symbols.

**Key finding — Gross margin distribution maps cleanly to taxonomy:**
- Tight envelope (<15%): LEA 7.0%, DAN 7.2%, CPS 7.5%, SUP 7.6%, AXL 10.0%
- Moderate envelope (15-30%): GTX 19.3%, SRI 20.9%, CMI 24.2%, THRM 25.6%
- Loose envelope (>30%): GNTX 33.8%, LFUS 37.5%, ALSN 47.5%

---

### 0.5 Sample Design Decision

**Date:** March 2, 2026

**Document:** `sample_design_recommendation.md`

**Decision: Three-layer sample, ~52 tickers requested.**

**Layer 1 — Deep Structural Analysis (10 firms):**
Original paired design with two replacements:
- ADNT → LCII (LCI Industries) — RV/specialty seating, publicly traded, SimFin available
- MOD → NXPI (NXP Semiconductors) — shifts pair to electronics/IP boundary, tests framework generalization

**Layer 2 — Statistical Validation (32 firms):**
Cross-subsector coverage across Tight, Moderate, and Loose envelopes. Includes aftermarket (DORM, SMP, LKQ), chemicals/materials (CE, EMN, RPM), electronics (ON, LFUS, TEL), and specialty (ALSN, FOXF, WGO).

**Layer 3 — Falsifiability Holdout (10 firms):**
Diversified industrials with auto exposure: CMI, ETN, EMR, PH, DOV, HON, ROK, ROP, IEX, TXT.

---

### 0.6 Expanded Pipeline Run — v3

**Date:** March 2, 2026

**Script:** `simfin_pipeline_v3.py`

**Outcome:**
- 46 of 52 tickers found (88.5% coverage)
- 830 total observations
- Layer 1: 10/10 found (all with full 19-quarter panels)
- Layer 2: 28/32 found (missing: HUN, PHIN, PPG, SNA)
- Layer 3: 8/10 found (missing: HON, TXT)

**Tickers to exclude (data quality):**

| Ticker | Issue | Quarters | Action |
|--------|-------|----------|--------|
| NN | -2,759% avg GM (data artifact) | 13 | Drop |
| HI | Only 1 quarter | 1 | Drop |
| ARNC | Below 15-quarter minimum | 13 | Drop |
| TEN | Went private (Apollo acquisition) | 10 | Drop |
| MPAA | Below 15-quarter minimum | 11 | Drop |

**Usable sample after exclusions: 41 firms, ~780 observations**
- Layer 1: 10 firms (190 observations)
- Layer 2: 23 firms (~430 observations)
- Layer 3: 8 firms (~150 observations)

**Taxonomy corrections from actual data:**
- VC (Visteon): Reclassify from Moderate to Tight (avg GM 10.7%, though trending up to 14.3%)
- GT (Goodyear): Reclassify from Tight to Moderate (avg GM 18.3%)

**Flag for investigation:**
- DAN (Dana Inc): Latest quarter GM of 1.5% vs. 11.4% average — potential one-time charge or restructuring. Verify against 10-K before treating as real margin behavior.

**New variables constructed in v3:**
- Cross-statement: cash conversion cycle, ROIC, accruals quality, capex intensity
- Rolling metrics: operating leverage, SGA stickiness, COGS ratio moving average
- All saved to `data/processed/` (10 CSV files + metadata JSON)

**Envelope distribution of usable sample:**
- Tight (<15%): 8 firms
- Moderate (15-30%): 29 firms
- Loose (>30%): 9 firms

---

## Statistical Power Assessment

With 41 usable firms × ~19 quarters = ~780 panel observations:
- Adequate for primary specification (system index + 2-3 key interactions)
- Firm-level clustering reduces effective sample size to ~41 independent units
- Robust standard errors at firm level are essential
- Not sufficient for saturated models with all 5 dimensions × multiple interactions
- Layer 3 holdout (8 firms) provides out-of-sample validation

---

## Decisions Log

| # | Date | Decision | Rationale | Impact |
|---|------|----------|-----------|--------|
| 1 | 2026-03-02 | Use VS Code + Terminal | Best balance of IDE features and terminal access for Python data work | Environment |
| 2 | 2026-03-02 | Bypass sf.load() with direct CSV reading | SimFin library incompatible with Python 3.13 + pandas 3.x | Data pipeline |
| 3 | 2026-03-02 | Replace ADNT with LCII | ADNT not in SimFin free tier; LCII is comparable seating/interiors pure-play | Sample design |
| 4 | 2026-03-02 | Replace MOD with NXPI | MOD not in SimFin; NXPI shifts pair to electronics/IP boundary | Sample design |
| 5 | 2026-03-02 | Three-layer sample: 10 + 32 + 10 | Balances depth (L1), statistical power (L2), and falsifiability (L3) | Research design |
| 6 | 2026-03-02 | Drop NN, HI, ARNC, TEN, MPAA | Data quality — insufficient quarters or anomalous data | Sample composition |
| 7 | 2026-03-02 | Minimum 15 quarters for inclusion | Need sufficient time series for rolling metrics (8-quarter window) | Data quality |

---

## Next Steps

1. **Commit current work to GitHub** — all scripts, documentation, processed data summaries
2. **Verify DAN Q4 2024 margin drop** — check SEC 10-K for one-time charges
3. **SEC EDGAR customer concentration scraper** — extract major customer disclosures for D1 (Network Position)
4. **FRED macro data pull** — PPI, capacity utilization, vehicle production for D3 (Elasticity proxy)
5. **Network topology construction** — OEM supplier list cross-referencing for D1
6. **Taxonomy assignment refinement** — use customer concentration + GM + subsector data to classify all 41 firms
7. **Variable codebook** — formal documentation of every variable, its construction, proxy assumptions, and which dimension it serves

---

## File Inventory

| File | Location | Purpose | Status |
|------|----------|---------|--------|
| simfin_pipeline.py | src/data_collection/ | Original 10-ticker pipeline (v1, uses sf.load — broken) | Superseded by v3 |
| simfin_pipeline_v3.py | src/data_collection/ | Expanded 52-ticker pipeline (direct CSV) | Current |
| simfin_discovery.py | src/data_collection/ | Universe discovery scan | Complete |
| requirements.txt | project root | Python dependencies | Current |
| .gitignore | project root | Excludes .env, data/raw/, .venv/ | Current |
| .env | project root | API keys (gitignored) | Active |
| sample_design_recommendation.md | docs/ | Sample design analysis and decisions | Complete |
| PROJECT_LOG.md | docs/ | This document | Living document |
| sample_metadata.json | data/processed/ | Layer assignments and pipeline config | Current |
| margin_variables.csv | data/processed/ | Gross margin, operating margin, COGS ratio, SGA ratio | Current |
| balance_sheet_variables.csv | data/processed/ | Working capital, debt ratios, asset intensity | Current |
| cashflow_variables.csv | data/processed/ | OCF, FCF, capex, depreciation | Current |
| rolling_metrics.csv | data/processed/ | GM volatility, COGS-revenue correlation, operating leverage | Current |
| cross_statement_variables.csv | data/processed/ | CCC, ROIC, accruals quality, capex intensity | Current |
| ticker_summary.csv | data/processed/ | Summary table with layer assignments | Current |
