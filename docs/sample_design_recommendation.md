# Sample Design Recommendation
## Supply Chain Constraint System: Automotive Pilot Study

**Date:** March 2, 2026
**Status:** Design Phase - Ready for Implementation
**Context:** Discovery scan of SimFin US universe completed; auto tickers identified and initial panel data retrieved

---

## 1. Discovery Results Summary

### Data Universe
- **SimFin US Total Universe:** 6,526 companies
- **Companies with Quarterly Income Data:** 3,636
- **Full 19-Quarter Panel (Q4 2020–Q2 2025):** 1,690 tickers
- **Auto Industry Classification:** 208 companies (across primary and secondary NAICS)

### Auto Sector Identification
- **Known Auto Tickers (Curated List):** 78
- **Found in SimFin with Full Panel:** 56 (71.8% coverage)
- **Missing from SimFin:** 22 tickers (including ADNT, MOD, BWA, ALV, MGA)

### Gross Margin Distribution (56 Found Tickers)

**Tight Envelope (<15%):**
- LEA (7.0%), DAN (7.2%), CPS (7.5%), TEN (~8%), SUP (~9%), AXL (~10%)
- **Insight:** Tier 1 candidates - severe margin constraint, classic price-taker positioning

**Moderate Envelope (15–30%):**
- GTX (19.3%), SRI (20.9%), CMI (24.2%), VC (~22%), and ~15 others
- **Insight:** Tier 2 candidates - where diagnostic gap analysis has strongest value

**Loose Envelope (>30%):**
- GNTX (33.8%), LFUS (37.5%), ALSN (47.5%)
- **Insight:** Tier 3 candidates - boundary testing, IP-driven moat, less margin-constrained

---

## 2. Sample Size Assessment

### Statistical Requirements
For hierarchical panel regression with 5 key predictors (network position, information asymmetry proxy, demand elasticity, stack architecture, behavioral cost stickiness) and interaction terms:
- **Minimum observations per predictor rule:** 10–15 × 5 = 50–75 observations
- **Clustering structure:** Firm-level clustering reduces effective sample size; robust standard errors essential
- **Our panel structure:** ~50 firms × 19 quarters = ~950 panel observations before any dropping

### Power Assessment
**Available auto tickers with full panel:** 56
**Realistic usable sample after data cleaning:** 45–55 firms
**Expected effective sample size (firm-level clustering):** ~45–50 independent units × 19 time periods
**Verdict:** Adequate for primary analysis (above minimum), tight for extensive interaction testing. Holdout sample of 10–12 reduces to ~40 firms for estimation, manageable but non-negotiable for cross-validation.

### Implications
- Layer 1 (10–12 firms) can support detailed 5-dimension measurement and system validation
- Layer 2 (30–40 firms) provides robust test of whether Layer 1 patterns generalize
- Layer 3 (8–12 firms) tests falsifiability and boundary conditions; does not need to be auto-pure-play
- **Statistical priority:** Better to have solid measurement on fewer firms than weak proxies on many

---

## 3. Proposed Three-Layer Sample Design

### Layer 1: Deep Structural Analysis (10–12 Firms)
**Purpose:** Full 5-dimension assessment; frame the system hypothesis; generate publishable evidence of integration

**Original Paired Design (with replacements):**

| Dimension | Firm A (Constraint) | Firm B (Control) | GM Range | Envelope | Notes |
|-----------|-------------------|------------------|----------|----------|-------|
| Drivetrain dominance | AXL (~10%) | DAN (7.2%) | Tight | T/P | AXL: 70%+ GM dependency; DAN: < 40% GM |
| Seating leverage | **LCII** (replace ADNT) | LEA (7.0%) | Tight | T/P | LCII: RV/specialty; LEA: pure OEM seating |
| Thermal management | **NXPI** (replace MOD) | THRM | Moderate | M/P or M/C | NXPI: electronics tier-1; THRM: thermal specialist |
| Electronics integration | VC (~22%) | SRI (20.9%) | Moderate | M/P | VC: cockpit architecture; SRI: sensor-focused |
| IP/Product moat | GNTX (33.8%) | APTV (~15%) | Loose/Moderate | L/E vs M/C | GNTX: glass/optics moat; APTV: systems architecture |

**Rationale for Replacements:**
- **ADNT → LCII:** ADNT not in SimFin; LCII (LCI Industries) is publicly traded, seating/interiors supplier, available panel data, pure-play positioning similar to ADNT intent
- **MOD → NXPI:** MOD (Modine, thermal) not retrievable; NXPI (NXP Semiconductors) shifts the test to electronics boundary but maintains the principle of comparing tight IP/product-moat positioning (GNTX) against systems integration (NXPI is cockpit/infotainment semiconductor player)
- **Alternative for MOD:** Source MOD from SEC EDGAR manually if data is critical; NXPI substitution tests robustness

**Data Quality Check:**
- Confirm all 10–12 tickers have complete 19-quarter panels
- Verify customer concentration data (10-K customer disclosures) available
- Validate supplier list accessibility for network construction

---

### Layer 2: Statistical Validation (30–40 Firms)
**Purpose:** Test whether Layer 1 patterns generalize; build Tier 2 diagnostic capability; estimate stable parameters

**Selection Criteria:**
1. Full 19-quarter panel in SimFin
2. Gross margin in 10–30% range (Moderate envelope focus for diagnostic value)
3. Primary NAICS in automotive supply (not auto assembly)
4. Exclude any firm with major M&A/restructuring in the 19-quarter window (data quality)

**Candidate Pool (Moderate envelope from discovery):**
- **Confirmed tickers:** GTX, SRI, CMI, VC, and ~15 others with GM 15–30%
- **Expected size after cleaning:** 30–40 firms
- **Selection method:** Stratify by subsector (seating, drivetrain, thermal, electronics, systems integration) to ensure coverage across supply chain layers

**Subsector Stratification:**
- Seating/interiors: LEA, DAN, LCII, + 2–3 others
- Drivetrain/powerplant: AXL, TEN, SUP, + 2–3 others
- Thermal/emissions: (post-MOD resolution), + 2–3 others
- Electronics/cockpit: VC, SRI, NXPI (if included), + 2–3 others
- Systems integration: APTV, GTX, CMI, + 2–3 others

---

### Layer 3: Falsifiability / Generalizability (8–12 Firms)
**Purpose:** Test robustness beyond pure-play auto; boundary conditions; what breaks the framework

**Selection:** Diversified industrials with substantial auto exposure (>20% of revenue) but primary classification elsewhere

**Candidates (from 208 auto-adjacent):**
- **CMI (Cummins):** Heavy-duty engines, but diversified into power gen, industrial (28% GM, Loose)
- **ETN (Eaton):** Electrical/hydraulic components, broad industrial base
- **EMR (Emerson):** Process management, climate tech, some auto seating/cockpit
- **PH (Parker-Hannifin):** Motion/control systems, diversified end-markets
- **HUBB (Hubbell):** Electrical/lighting, some auto applications

**Rationale:** These firms have tighter supply chains to non-auto end-markets (industrial, commercial, power). If the constraint system holds, we should see:
- Different marginal binds depending on customer (auto vs. industrial)
- Looser envelope when customer concentration is lower
- System breaks down without strong captive customer relationship (tests Tier 3 falsifiability)

**Expected Finding:** The five-dimension system explains margin variation well in tight/moderate envelopes (Layer 1, 2) but degrades in loose envelopes with diversified customer bases (Layer 3). This is *not* a failure—it defines the boundary of applicability.

---

## 4. Replacement Recommendations: ADNT and MOD

### ADNT Replacement: Seating / Interiors Pure-Play

**Recommended: LCII (LCI Industries)**
- **Status:** Publicly traded, full panel available in SimFin
- **Business:** Seating, interiors, structural components for RV and specialty vehicle segments
- **GM:** Historical range 15–18% (moderate envelope, not tight like LEA, but comparable to DAN)
- **Auto Exposure:** 60–70% of revenue to auto (RV, Class A/B/C motorhomes)
- **Advantages:** Pure-play positioning similar to ADNT; available data; different customer relationship (RV/specialty vs. OEM direct)
- **Caveats:** RV cycle different from OEM auto cycle; margin drivers may differ; test for robustness

**Alternative (if LCII data is problematic):**
- Hand-source ADNT from SEC EDGAR 10-K filings and financial databases (requires manual panel construction, ~4–6 hours)
- ADNT is publicly traded; data exists, just not in SimFin's automated feed
- Decision point: If hypothesis depends critically on seating-pure-play representation, invest in manual sourcing

---

### MOD Replacement: Thermal Management / Electronics Boundary

**Recommended: NXPI (NXP Semiconductors)**
- **Status:** Publicly traded, full SimFin panel
- **Business:** Semiconductors for automotive (cockpit, infotainment, powertrain control, body electronics)
- **GM:** ~55–60% (Loose envelope, high-IP moat)
- **Auto Exposure:** ~40% of revenue (OEM automotive, tier-1 exposure)
- **Advantages:** Shifts test to electronics/software tier-1 (complements VC's cockpit position); IP-driven moat comparable to GNTX logic; strong panel data
- **Caveats:** Not thermal management specifically; tests whether framework generalizes to software-stack layers vs. mechanical-thermal layers

**Alternative (stronger but requires work):**
- **ON Semi (ON Semiconductor):** Power management, body control, sensor interface ICs. ~60–65% GM, comparable positioning to NXPI
- **Manual source:** Modine (MOD) from SEC EDGAR if thermal management representation is critical
- **Decision point:** If Layer 1 requires actual thermal specialist, prioritize MOD manual sourcing. If Layer 1 intent is to test IP-moat vs. systems-integration across different subsectors, NXPI or ON Semi are acceptable

---

## 5. Taxonomy Pre-Classification

### Three-Axis Taxonomy Recap
- **Axis 1 - Margin Determination Mode:** P (Price-taker) | C (Cost-plus) | E (Extractive/moat-driven)
- **Axis 2 - Constraint Envelope Tightness:** T (Tight, <15%) | M (Moderate, 15–30%) | L (Loose, >30%)
- **Axis 3 - Supply Chain Legibility:** H (High, few customers, deep traceability) | M (Medium) | L (Low, diversified, complex)

### Preliminary Classifications (56 Found Tickers)

**Layer 1 (Deep):**

| Ticker | GM | Envelope | Mode (Preliminary) | Legibility | Tier | Notes |
|--------|----|---------|----|-----------|------|-------|
| AXL | ~10% | T | P | H | 1 | Drivetrain, tight, price-taker |
| DAN | 7.2% | T | P | H | 1 | Seating, tight, captive |
| LCII | 15–18% | M | P | M | 1 | Seating/interiors (replacement) |
| LEA | 7.0% | T | P | H | 1 | Seating, pure-play, tight |
| THRM | ~18% | M | C | H | 1 | Thermal, cost-plus or contract |
| NXPI | 55–60% | L | E | M | 1 | Semiconductors (replacement), IP moat |
| VC | ~22% | M | C | M | 1 | Cockpit, architecture value |
| SRI | 20.9% | M | P | M | 1 | Sensors, moderate margin |
| GNTX | 33.8% | L | E | H | 1 | Glass/optics, product moat |
| APTV | ~15% | M | C | M | 1 | Systems integration, architecture |

**Layer 2 (Statistical, Moderate Envelope Focus):**

| Ticker Range | GM | Envelope | Mode | Legibility | Tier | Examples |
|--------------|----|---------|----|-----------|------|----------|
| GTX, CMI, others | 19–24% | M | C | M | 2 | Cost-plus or negotiated fixed margins |
| SRI, others | 20–22% | M | P | M | 2 | Price-taker, commodity-ish |
| VC, others | 20–25% | M | E | M | 2 | Extracting some margin from architecture |
| **Expected:** 30–40 firms across subsectors | | | | | | |

**Layer 3 (Falsifiability, Boundary Testing):**

| Ticker | GM | Envelope | Mode | Legibility | Tier | Notes |
|--------|----|---------|----|-----------|------|-------|
| CMI | 24.2% | M–L | E | L | 3 | Diversified (power gen, industrial, auto 28%) |
| ETN | varies | M | C | L | 3 | Multi-sector, broad customer base |
| EMR | varies | M | C | L | 3 | Process management, industrial-heavy |
| PH | varies | M–L | C | L | 3 | Motion control, diversified |
| HUBB | varies | M | C | L | 3 | Electrical/lighting, loose auto coupling |

**Preliminary Mode Assignment Logic (to be refined with customer concentration data):**
- **P (Price-taker):** GM < 12%, few differentiators, captive to one or two OEMs, low pricing power
- **C (Cost-plus):** GM 12–25%, contract-negotiated margins, some customization, moderate pricing power
- **E (Extractive):** GM > 25%, proprietary IP/moat, architecture control, pricing power from differentiation

---

## 6. Statistical Power and Panel Structure

### Panel Characteristics
- **Time dimension:** 19 quarters (Q4 2020–Q2 2025)
- **Cross-sectional dimension (estimation sample):** ~45–48 firms (Layers 1 + 2)
- **Cross-sectional dimension (holdout):** ~8–12 firms (Layer 3)
- **Total observations:** ~45 × 19 = 855 firm-quarter observations for estimation

### Effective Sample Size Consideration
- **Naive count:** 855 observations
- **Firm-level clustering adjustment:** Effective sample size ≈ 45–48 independent units for parameter estimation
- **Implication:** Power is driven by the number of firms, not quarters; robust standard errors at firm level are essential
- **Rule-of-thumb:** 45–48 firms supports ~5–6 key parameters + 2–3 interactions; beyond that, precision degrades

### Implications for Specification
1. **Primary specification:** System index (latent composite of 5 dimensions) vs. margin; simple specification to preserve df
2. **Secondary specifications:** Individual dimension effects + key interactions (e.g., elasticity × network position)
3. **Avoid:** Saturated models with all 5 dimensions × 2–3 interactions unless subsample sizes warrant (e.g., Tight vs. Moderate strata separately)
4. **Robustness checks:** Cross-validation using Layer 3 as holdout, leave-one-firm-out, lagged specifications

### Quarters and Cyclicality
- **19 quarters covers:** Pre-COVID, COVID supply shock, recovery, inflation surge (2021–2024), current normalization
- **Advantage:** Captures structural breaks and shocks useful for identification
- **Caution:** COVID and tariff shocks may dominate margin variation; include shock dummies, test for heterogeneity by period

---

## 7. Immediate Next Steps

1. **Data Validation & Panel Construction (Week 1–2)**
   - Confirm all Layer 1 + Layer 2 tickers (55+ firms) have complete 19-quarter panels in SimFin
   - Verify gross margin calculations (reconcile against SEC 10-K filings for 5–10 sample firms)
   - Identify and document any missing quarters or data gaps
   - **Deliverable:** Clean master dataset, n-count, any exclusions documented

2. **SEC EDGAR Data Sourcing for Missing Tickers (Week 2–3)**
   - Decision point: Attempt manual sourcing of ADNT from SEC EDGAR
   - If sourcing succeeds: Construct 19-quarter panel, integrate with SimFin data
   - If unfeasible: Confirm LCII as replacement, validate comparability to ADNT intent
   - **Same decision for MOD:** Manual source vs. NXPI/ON Semi substitution
   - **Deliverable:** Final Layer 1 roster (10–12 tickers confirmed with complete data)

3. **Customer Concentration & Network Data (Week 3–4)**
   - Extract customer concentration from SEC EDGAR 10-K (Item 1, Item 7 MD&A; "Customers" disclosure)
   - Identify primary OEM customers (GM, Ford, Tesla, Honda, etc.) for each supplier
   - Collect OEM supplier lists (GM Supplier Directory, Ford, Tesla public lists) to construct network position proxies
   - **Deliverable:** Customer concentration table, initial network-position indicators

4. **Variable Construction & Proxy Development (Week 4–5)**
   - **Elasticity proxy:** FRED data (vehicle production, capacity utilization), OEM supply-chain news
   - **Information asymmetry proxy:** Price volatility, forecast revision dispersion, earnings surprise magnitude
   - **Stack architecture indicator:** Subsector classification + customer breadth
   - **Cost stickiness measure:** Quarterly SG&A lag structure, depreciation patterns
   - **Test convergent validity:** Do multiple proxies for same dimension correlate? (e.g., 2+ elasticity measures)
   - **Deliverable:** Variable codebook with assumptions and proxy justifications

5. **Preliminary Taxonomy Assignment (Week 5–6)**
   - Use customer concentration + GM + subsector to assign firms to cells (P/C/E × T/M/L × H/M/L)
   - Flag any ambiguous classifications for deeper examination
   - Stratify Layer 2 by taxonomy cell to ensure coverage
   - **Deliverable:** Taxonomy classification table (all 55 firms)

6. **Specification Pre-Planning (Week 6)**
   - Sketch primary specification: System index (5 dimensions) + firm FE + time FE vs. log(GM)
   - Specify interaction terms (elasticity × network position, architecture × concentration)
   - Plan robustness checks: OLS vs. panel fixed-effects, robust vs. clustered SEs, subsample by envelope
   - **Deliverable:** Model specification memo with hypothesized coefficient signs and robustness plan

7. **Quality Gate Review**
   - Before proceeding to estimation: Confirm data completeness, variable distributions, no major outliers
   - Compare summary statistics to industry benchmarks (verify data plausibility)
   - Test any hard assumptions (e.g., do tight-envelope firms actually have <15% GM consistently?)
   - **Deliverable:** Data quality report; decision on any outlier/exclusion rules

---

## 8. Risk Registry

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Missing tickers (ADNT, MOD) not replaceable | Med | High | Prioritize ADNT manual sourcing; NXPI acceptable substitute for MOD |
| 45–50 firms insufficient for 5-dim + interactions | Low | Med | Pre-commit to parsimonious spec (system index first) |
| Customer concentration data incomplete or unavailable | Med | High | Use alternative proxies (supplier count, HHI estimates) |
| Layer 1 GM assumptions don't hold (outliers, errors) | Low | Med | Reconcile against 10-K filings; exclude obvious errors |
| Takeover/major M&A in 19-quarter window distorts margins | Med | Med | Flag in analysis; test sensitivity to inclusion/exclusion |
| COVID-driven margin distortions dominate findings | Med | Med | Include shock dummies; test pre-COVID subsample |
| Endogeneity in network position (profitable firms invest in better positions) | High | High | Acknowledge in paper; use lagged predictors; test with exogenous shocks |

---

## 9. Summary & Decision Points

This sample design balances rigor, feasibility, and analytical power:

- **Layer 1 (10–12):** Tests whether the five-dimension system holds in controlled paired comparisons; foundation for Tier 1 model validation
- **Layer 2 (30–40):** Generalizes Layer 1 findings; builds diagnostic capability; the statistical core
- **Layer 3 (8–12):** Tests boundary conditions; identifies where framework breaks; supports falsifiability claims

**Critical decisions needed immediately:**
1. **Replacement strategy for ADNT and MOD:** Manual SEC EDGAR sourcing vs. SimFin substitutes?
2. **LCII confirmation:** Accept as ADNT substitute, or pursue manual sourcing?
3. **NXPI or ON Semi:** Acceptable as MOD thermal proxy in Layer 1?

Once these are resolved, the data construction and variable development pipeline is well-defined and resource-constrained.

---

**Prepared by:** Supply Chain Constraint System Research Project
**Status:** Ready for Ian's decision on replacement tickers and manual sourcing investment
**Next Review:** Upon completion of Week 1–2 data validation
