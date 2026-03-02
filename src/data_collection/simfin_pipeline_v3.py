"""
SimFin Data Pipeline v3 — Supply Chain Constraint System
========================================================
Expanded sample: ~55 firms across three analytical layers.
Bypasses sf.load() to work with Python 3.13 + pandas 3.x.

Usage:
    python src/data_collection/simfin_pipeline_v3.py

Requires:
    - .env file with SIMFIN_API_KEY=your_key
    - pip install simfin pandas numpy python-dotenv
"""

import os
import simfin as sf
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()
API_KEY = os.getenv('SIMFIN_API_KEY')
if not API_KEY:
    raise ValueError("SIMFIN_API_KEY not found in .env file")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SIMFIN_DATA_DIR = PROJECT_ROOT / 'data' / 'raw' / 'simfin'
OUTPUT_DIR = PROJECT_ROOT / 'data' / 'processed'

sf.set_api_key(api_key=API_KEY)
sf.set_data_dir(str(SIMFIN_DATA_DIR))

# Minimum quarters required for inclusion
MIN_QUARTERS = 15

# ============================================================
# THREE-LAYER SAMPLE DESIGN
# ============================================================

# Layer 1: Deep structural analysis (10-12 firms)
# Full 5-dimension assessment, paired design
LAYER_1 = {
    'AXL':  {'name': 'American Axle',    'pair': 'drivetrain',    'envelope': 'T', 'mode': 'P'},
    'DAN':  {'name': 'Dana Inc',         'pair': 'drivetrain',    'envelope': 'T', 'mode': 'P'},
    'LCII': {'name': 'LCI Industries',   'pair': 'seating',       'envelope': 'M', 'mode': 'P'},
    'LEA':  {'name': 'Lear Corp',        'pair': 'seating',       'envelope': 'T', 'mode': 'P'},
    'THRM': {'name': 'Gentherm',         'pair': 'thermal',       'envelope': 'M', 'mode': 'C'},
    'NXPI': {'name': 'NXP Semiconductors','pair': 'electronics_IP','envelope': 'L', 'mode': 'E'},
    'VC':   {'name': 'Visteon',          'pair': 'electronics',   'envelope': 'M', 'mode': 'C'},
    'SRI':  {'name': 'Stoneridge',       'pair': 'electronics',   'envelope': 'M', 'mode': 'P'},
    'GNTX': {'name': 'Gentex',           'pair': 'IP_moat',       'envelope': 'L', 'mode': 'E'},
    'APTV': {'name': 'Aptiv',            'pair': 'IP_moat',       'envelope': 'M', 'mode': 'C'},
}

# Layer 2: Statistical validation (30-40 firms)
# Moderate envelope focus, cross-subsector coverage
LAYER_2 = {
    # --- Tight envelope (GM < 15%) ---
    'CPS':  {'name': 'Cooper-Standard',   'subsector': 'seating_rubber',  'envelope': 'T', 'mode': 'P'},
    'SUP':  {'name': 'Superior Industries','subsector': 'wheels',         'envelope': 'T', 'mode': 'P'},
    'TEN':  {'name': 'Tenneco',           'subsector': 'emissions',       'envelope': 'T', 'mode': 'P'},
    'GT':   {'name': 'Goodyear Tire',     'subsector': 'tires',           'envelope': 'T', 'mode': 'P'},
    'NN':   {'name': 'NN Inc',            'subsector': 'precision_parts', 'envelope': 'T', 'mode': 'P'},

    # --- Moderate envelope (GM 15-30%) ---
    'GTX':  {'name': 'Garrett Motion',    'subsector': 'turbo_emissions', 'envelope': 'M', 'mode': 'C'},
    'DORM': {'name': 'Dorman Products',   'subsector': 'aftermarket',     'envelope': 'M', 'mode': 'C'},
    'SMP':  {'name': 'Standard Motor Products','subsector': 'aftermarket','envelope': 'M', 'mode': 'C'},
    'ITT':  {'name': 'ITT Inc',           'subsector': 'connectors',      'envelope': 'M', 'mode': 'C'},
    'MEI':  {'name': 'Methode Electronics','subsector': 'electronics',    'envelope': 'M', 'mode': 'P'},
    'BDC':  {'name': 'Belden Inc',        'subsector': 'connectivity',    'envelope': 'M', 'mode': 'C'},
    'ST':   {'name': 'Sensata Technologies','subsector': 'sensors',       'envelope': 'M', 'mode': 'C'},
    'MPAA': {'name': 'Motorcar Parts America','subsector': 'aftermarket', 'envelope': 'M', 'mode': 'P'},
    'ARNC': {'name': 'Arconic',           'subsector': 'materials',       'envelope': 'M', 'mode': 'P'},
    'PHIN': {'name': 'PHINIA Inc',        'subsector': 'fuel_systems',    'envelope': 'M', 'mode': 'C'},
    'HI':   {'name': 'Hillenbrand',       'subsector': 'industrial_equip','envelope': 'M', 'mode': 'C'},
    'FOXF': {'name': 'Fox Factory',       'subsector': 'suspension',      'envelope': 'M', 'mode': 'E'},
    'LKQ':  {'name': 'LKQ Corp',         'subsector': 'aftermarket',     'envelope': 'M', 'mode': 'C'},
    'GPC':  {'name': 'Genuine Parts Co',  'subsector': 'distribution',    'envelope': 'M', 'mode': 'C'},
    'SNA':  {'name': 'Snap-on',           'subsector': 'tools',           'envelope': 'M', 'mode': 'E'},
    'WGO':  {'name': 'Winnebago',         'subsector': 'RV_OEM',          'envelope': 'M', 'mode': 'C'},
    'MNRO': {'name': 'Monro Inc',         'subsector': 'aftermarket_svc', 'envelope': 'M', 'mode': 'C'},

    # --- Loose envelope (GM > 30%) ---
    'ALSN': {'name': 'Allison Transmission','subsector': 'transmission',  'envelope': 'L', 'mode': 'E'},
    'LFUS': {'name': 'Littelfuse',        'subsector': 'electronics',     'envelope': 'L', 'mode': 'E'},
    'ON':   {'name': 'ON Semiconductor',  'subsector': 'semiconductors',  'envelope': 'L', 'mode': 'E'},
    'TEL':  {'name': 'TE Connectivity',   'subsector': 'connectors',      'envelope': 'L', 'mode': 'E'},

    # --- Materials/Chemical suppliers ---
    'CE':   {'name': 'Celanese',          'subsector': 'chemicals',       'envelope': 'M', 'mode': 'C'},
    'EMN':  {'name': 'Eastman Chemical',  'subsector': 'chemicals',       'envelope': 'M', 'mode': 'C'},
    'PPG':  {'name': 'PPG Industries',    'subsector': 'coatings',        'envelope': 'M', 'mode': 'C'},
    'HUN':  {'name': 'Huntsman Corp',     'subsector': 'chemicals',       'envelope': 'M', 'mode': 'P'},
    'RPM':  {'name': 'RPM International', 'subsector': 'coatings',        'envelope': 'M', 'mode': 'C'},
    'TROX': {'name': 'Tronox',            'subsector': 'titanium',        'envelope': 'M', 'mode': 'P'},
}

# Layer 3: Falsifiability / generalizability holdout (8-12 firms)
# Diversified industrials with auto exposure — tests boundary conditions
LAYER_3 = {
    'CMI':  {'name': 'Cummins',           'subsector': 'engines_power',   'envelope': 'M', 'mode': 'C'},
    'ETN':  {'name': 'Eaton Corp',        'subsector': 'electrical_hyd',  'envelope': 'M', 'mode': 'C'},
    'EMR':  {'name': 'Emerson Electric',  'subsector': 'automation',      'envelope': 'M', 'mode': 'C'},
    'PH':   {'name': 'Parker Hannifin',   'subsector': 'motion_control',  'envelope': 'M', 'mode': 'C'},
    'DOV':  {'name': 'Dover Corp',        'subsector': 'diversified',     'envelope': 'M', 'mode': 'C'},
    'HON':  {'name': 'Honeywell',         'subsector': 'diversified',     'envelope': 'L', 'mode': 'E'},
    'ROK':  {'name': 'Rockwell Automation','subsector': 'automation',     'envelope': 'L', 'mode': 'E'},
    'TXT':  {'name': 'Textron',           'subsector': 'diversified',     'envelope': 'M', 'mode': 'C'},
    'IEX':  {'name': 'IDEX Corp',         'subsector': 'pumps_flow',      'envelope': 'L', 'mode': 'E'},
    'ROP':  {'name': 'Roper Technologies','subsector': 'diversified_tech','envelope': 'L', 'mode': 'E'},
}

# Combined roster
ALL_TICKERS = {}
for d, layer_name in [(LAYER_1, 'L1'), (LAYER_2, 'L2'), (LAYER_3, 'L3')]:
    for ticker, info in d.items():
        ALL_TICKERS[ticker] = {**info, 'layer': layer_name}

TICKER_LIST = list(ALL_TICKERS.keys())

print(f"Sample design: {len(LAYER_1)} Layer 1 + {len(LAYER_2)} Layer 2 + {len(LAYER_3)} Layer 3 = {len(ALL_TICKERS)} total")


# ============================================================
# DIRECT CSV LOADING (bypasses sf.load() — Python 3.13 fix)
# ============================================================

def ensure_downloaded(dataset, variant='quarterly', market='us'):
    """Trigger SimFin download, then read CSV directly."""
    try:
        sf.load(dataset=dataset, variant=variant, market=market)
    except TypeError:
        pass  # Expected: date_parser bug in simfin + pandas 3.x
    except Exception as e:
        print(f"  Download trigger for {dataset}: {e}")


def load_csv_direct(dataset, variant='quarterly'):
    """Read SimFin CSV directly with modern pandas."""
    # Map dataset names to file patterns
    file_map = {
        'income': f'us-income-{variant}.csv',
        'balance': f'us-balance-{variant}.csv',
        'cashflow': f'us-cashflow-{variant}.csv',
    }

    filepath = SIMFIN_DATA_DIR / file_map[dataset]

    if not filepath.exists():
        print(f"  File not found: {filepath}")
        print(f"  Triggering download...")
        ensure_downloaded(dataset, variant)

    if not filepath.exists():
        # Try alternate patterns
        for f in SIMFIN_DATA_DIR.iterdir():
            if dataset in f.name.lower() and variant in f.name.lower() and f.suffix == '.csv':
                filepath = f
                break

    if not filepath.exists():
        raise FileNotFoundError(f"Cannot find {dataset} {variant} CSV in {SIMFIN_DATA_DIR}")

    print(f"  Reading {filepath.name}...")
    df = pd.read_csv(
        filepath,
        sep=';',
        parse_dates=['Report Date', 'Publish Date', 'Restated Date'],
    )

    # Filter to our tickers
    df = df[df['Ticker'].isin(TICKER_LIST)].copy()
    df = df.set_index(['Ticker', 'Report Date']).sort_index()

    found_tickers = df.index.get_level_values('Ticker').unique()
    print(f"  {dataset.title()}: {len(df)} rows, {len(found_tickers)}/{len(TICKER_LIST)} tickers found")

    missing = set(TICKER_LIST) - set(found_tickers)
    if missing:
        print(f"  Missing tickers: {sorted(missing)}")

    return df


# ============================================================
# VARIABLE CONSTRUCTION — Framework Dimensions
# ============================================================

def safe_col(df, col_name, alt_names=None):
    """Safely get a column, trying alternates if needed."""
    if col_name in df.columns:
        return df[col_name]
    if alt_names:
        for alt in alt_names:
            if alt in df.columns:
                return df[alt]
    return pd.Series(np.nan, index=df.index, dtype='float64')


def construct_margin_variables(income_df):
    """
    Construct margin variables from income statements.

    Feeds into:
    - Dependent variable: Gross margin (GM)
    - D5 (Behavioral Margin Sensitivity): margin volatility, adjustment speed
    - D4 (Stack Architecture): COGS/Revenue ratio
    - D2 (Information Asymmetry proxy): SGA/Revenue ratio
    """
    print("\nConstructing margin variables...")

    v = pd.DataFrame(index=income_df.index)

    v['revenue'] = safe_col(income_df, 'Revenue')
    v['cogs'] = safe_col(income_df, 'Cost of Revenue', ['Cost of Goods Sold', 'COGS'])
    v['gross_profit'] = safe_col(income_df, 'Gross Profit')
    v['operating_income'] = safe_col(income_df, 'Operating Income (Loss)',
                                     ['Operating Income', 'EBIT'])
    v['sga'] = safe_col(income_df, 'Selling, General & Administrative',
                        ['SG&A', 'Selling General & Administrative'])
    v['rd_expense'] = safe_col(income_df, 'Research & Development',
                               ['R&D Expense', 'Research and Development'])
    v['net_income'] = safe_col(income_df, 'Net Income', ['Net Income Common'])

    # Margin ratios
    v['gross_margin'] = v['gross_profit'] / v['revenue']
    v['operating_margin'] = v['operating_income'] / v['revenue']
    v['cogs_to_revenue'] = v['cogs'] / v['revenue']
    v['sga_to_revenue'] = v['sga'] / v['revenue']
    v['rd_to_revenue'] = v['rd_expense'] / v['revenue']
    v['net_margin'] = v['net_income'] / v['revenue']

    print(f"  Margin variables: {len(v)} observations, "
          f"{v.index.get_level_values('Ticker').nunique()} tickers")
    return v


def construct_balance_sheet_variables(balance_df):
    """
    Construct balance sheet variables.

    Feeds into:
    - D2 (Information Asymmetry): inventory metrics, working capital
    - D5 (Behavioral): asset intensity, capital structure
    - Economic profit decomposition: invested capital, ROIC
    """
    print("Constructing balance sheet variables...")

    v = pd.DataFrame(index=balance_df.index)

    v['total_assets'] = safe_col(balance_df, 'Total Assets')
    v['inventory'] = safe_col(balance_df, 'Inventories', ['Inventory'])
    v['accounts_receivable'] = safe_col(balance_df, 'Accounts & Notes Receivable',
                                        ['Accounts Receivable', 'Trade Receivables'])
    v['accounts_payable'] = safe_col(balance_df, 'Payables & Accruals',
                                     ['Accounts Payable', 'Trade Payables',
                                      'Accounts Payable & Accrued Liabilities'])
    v['total_current_assets'] = safe_col(balance_df, 'Total Current Assets')
    v['total_current_liabilities'] = safe_col(balance_df, 'Total Current Liabilities')
    v['total_debt'] = safe_col(balance_df, 'Total Debt',
                               ['Short Term Debt', 'Long Term Debt'])
    v['long_term_debt'] = safe_col(balance_df, 'Long Term Debt')
    v['total_equity'] = safe_col(balance_df, 'Total Equity')
    v['pp_and_e'] = safe_col(balance_df, 'Property, Plant & Equipment, Net',
                             ['Property Plant & Equipment Net', 'Net PP&E'])
    v['intangibles'] = safe_col(balance_df, 'Intangible Assets',
                                ['Goodwill & Intangibles'])
    v['goodwill'] = safe_col(balance_df, 'Goodwill')

    # Derived metrics
    v['net_working_capital'] = v['total_current_assets'] - v['total_current_liabilities']
    v['current_ratio'] = v['total_current_assets'] / v['total_current_liabilities']
    v['inventory_to_assets'] = v['inventory'] / v['total_assets']
    v['ar_to_assets'] = v['accounts_receivable'] / v['total_assets']
    v['debt_to_equity'] = v['total_debt'] / v['total_equity']
    v['debt_to_assets'] = v['total_debt'] / v['total_assets']
    v['asset_intensity'] = v['pp_and_e'] / v['total_assets']
    v['intangible_ratio'] = v['intangibles'] / v['total_assets']

    # Cash conversion cycle components (will combine with income data later)
    # Days inventory = Inventory / (COGS/365)
    # Days receivable = AR / (Revenue/365)
    # Days payable = AP / (COGS/365)

    print(f"  Balance sheet variables: {len(v)} observations, "
          f"{v.index.get_level_values('Ticker').nunique()} tickers")
    return v


def construct_cashflow_variables(cashflow_df):
    """
    Construct cash flow variables.

    Feeds into:
    - Economic profit decomposition: FCF, capex intensity
    - D5 (Behavioral): capex patterns, cash conversion
    """
    print("Constructing cash flow variables...")

    v = pd.DataFrame(index=cashflow_df.index)

    v['operating_cashflow'] = safe_col(cashflow_df, 'Net Cash from Operating Activities',
                                       ['Cash from Operations', 'Operating Cash Flow'])
    v['capex'] = safe_col(cashflow_df, 'Change in Fixed Assets & Intangibles',
                          ['Capital Expenditures', 'Purchase of Property Plant & Equipment',
                           'Acquisition of Fixed Assets & Intangibles'])
    v['depreciation'] = safe_col(cashflow_df, 'Depreciation & Amortization',
                                  ['D&A', 'Depreciation and Amortization'])
    v['dividends'] = safe_col(cashflow_df, 'Dividends Paid',
                               ['Cash Dividends Paid'])
    v['share_repurchase'] = safe_col(cashflow_df, 'Net Change in Debt',
                                     ['Repurchase of Common & Preferred Stock'])

    # Free cash flow (capex is typically negative)
    v['free_cashflow'] = v['operating_cashflow'] + v['capex']

    print(f"  Cash flow variables: {len(v)} observations, "
          f"{v.index.get_level_values('Ticker').nunique()} tickers")
    return v


# ============================================================
# ROLLING / PANEL METRICS (Dimension-specific)
# ============================================================

def construct_rolling_metrics(margin_df, window=8):
    """
    Construct rolling metrics for D5 (Behavioral Margin Sensitivity).
    Window = 8 quarters (2 years) by default.

    D5 variables:
    - Margin volatility (rolling std dev of gross margin)
    - Margin adjustment speed (autocorrelation of margin changes)
    - COGS-revenue correlation (cost-plus indicator: high = cost-plus)
    - Revenue volatility (feeds into D3 elasticity proxy)
    """
    print(f"\nConstructing rolling metrics (window={window} quarters)...")

    frames = []

    for ticker in margin_df.index.get_level_values('Ticker').unique():
        td = margin_df.loc[ticker].sort_index()

        r = pd.DataFrame(index=td.index)

        # D5: Gross margin volatility
        r['gm_volatility'] = td['gross_margin'].rolling(window=window, min_periods=4).std()
        r['gm_rolling_mean'] = td['gross_margin'].rolling(window=window, min_periods=4).mean()

        # D5: Quarter-over-quarter margin change
        r['gm_change'] = td['gross_margin'].diff()
        r['gm_change_abs'] = td['gross_margin'].diff().abs()

        # D5: COGS-Revenue correlation (cost-plus indicator)
        r['cogs_rev_corr'] = (
            td['cogs'].rolling(window=window, min_periods=4)
            .corr(td['revenue'])
        )

        # D3/D5: Revenue volatility
        r['revenue_volatility'] = (
            td['revenue'].pct_change()
            .rolling(window=window, min_periods=4).std()
        )

        # D5: Operating leverage (how much does operating income move per revenue change)
        rev_pct = td['revenue'].pct_change()
        oi_pct = td['operating_income'].pct_change()
        r['operating_leverage'] = (
            oi_pct.rolling(window=window, min_periods=4)
            .corr(rev_pct)
        )

        # D4: COGS ratio trend direction
        r['cogs_ratio_ma'] = td['cogs_to_revenue'].rolling(window=window, min_periods=4).mean()

        # D5: SGA stickiness (SGA volatility relative to revenue volatility)
        sga_pct = td['sga_to_revenue'].pct_change()
        r['sga_stickiness'] = (
            sga_pct.rolling(window=window, min_periods=4).std()
        )

        # Add ticker index
        r['Ticker'] = ticker
        r = r.set_index('Ticker', append=True).swaplevel()
        frames.append(r)

    rolling_df = pd.concat(frames)
    print(f"  Rolling metrics: {len(rolling_df)} observations, "
          f"{rolling_df.index.get_level_values('Ticker').nunique()} tickers")
    return rolling_df


# ============================================================
# CROSS-STATEMENT DERIVED VARIABLES
# ============================================================

def construct_cross_statement_variables(margin_df, balance_df, cashflow_df):
    """
    Variables that require data from multiple statements.

    Key outputs:
    - Cash conversion cycle (D2 proxy: inventory + AR - AP days)
    - ROIC (economic profit decomposition)
    - Capex intensity (D4/D5)
    - Accruals quality (D2 proxy: cash vs accrual earnings divergence)
    """
    print("\nConstructing cross-statement variables...")

    # Align on common index
    common_idx = margin_df.index.intersection(balance_df.index).intersection(cashflow_df.index)
    print(f"  Common observations across all three statements: {len(common_idx)}")

    v = pd.DataFrame(index=common_idx)

    m = margin_df.loc[common_idx]
    b = balance_df.loc[common_idx]
    c = cashflow_df.loc[common_idx]

    # Cash conversion cycle components (quarterly, so /91.25 days)
    quarterly_days = 91.25
    daily_cogs = m['cogs'] / quarterly_days
    daily_revenue = m['revenue'] / quarterly_days

    v['days_inventory'] = b['inventory'] / daily_cogs
    v['days_receivable'] = b['accounts_receivable'] / daily_revenue
    v['days_payable'] = b['accounts_payable'] / daily_cogs
    v['cash_conversion_cycle'] = v['days_inventory'] + v['days_receivable'] - v['days_payable']

    # Capex intensity
    v['capex_to_revenue'] = c['capex'].abs() / m['revenue']
    v['capex_to_assets'] = c['capex'].abs() / b['total_assets']

    # ROIC approximation: NOPAT / Invested Capital
    # NOPAT = Operating Income * (1 - tax rate), approximate tax rate as 21%
    tax_rate = 0.21
    v['nopat'] = m['operating_income'] * (1 - tax_rate)
    v['invested_capital'] = b['total_equity'] + b['total_debt'] if 'total_debt' in b.columns else b['total_equity']
    v['roic'] = v['nopat'] / v['invested_capital']

    # Accruals quality (D2 proxy)
    # High accruals relative to cash = potential information asymmetry / earnings management
    v['accruals'] = m['net_income'] - c['operating_cashflow']
    v['accruals_to_assets'] = v['accruals'] / b['total_assets']

    # Cash flow quality
    v['ocf_to_net_income'] = c['operating_cashflow'] / m['net_income']

    print(f"  Cross-statement variables: {len(v)} observations, "
          f"{v.index.get_level_values('Ticker').nunique()} tickers")
    return v


# ============================================================
# DATA QUALITY & REPORTING
# ============================================================

def data_quality_report(margin_df, balance_df, cashflow_df):
    """Comprehensive data quality summary by layer."""
    print("\n" + "=" * 70)
    print("DATA QUALITY REPORT")
    print("=" * 70)

    for layer_name, layer_dict in [('LAYER 1 (Deep)', LAYER_1),
                                    ('LAYER 2 (Statistical)', LAYER_2),
                                    ('LAYER 3 (Holdout)', LAYER_3)]:
        print(f"\n{'─' * 50}")
        print(f"  {layer_name}: {len(layer_dict)} tickers")
        print(f"{'─' * 50}")

        found_count = 0
        for ticker in sorted(layer_dict.keys()):
            info = layer_dict[ticker]
            in_data = ticker in margin_df.index.get_level_values('Ticker')

            if in_data:
                found_count += 1
                td = margin_df.loc[ticker]
                n_q = len(td)
                date_range = f"{td.index.min().strftime('%Y-%m')} to {td.index.max().strftime('%Y-%m')}"
                avg_gm = td['gross_margin'].mean()
                null_pct = td.isnull().mean().mean() * 100
                status = "OK" if n_q >= MIN_QUARTERS else f"LOW ({n_q}q)"
                print(f"  {ticker:6s} {info['name']:28s} {n_q:2d}q  GM={avg_gm:5.1%}  "
                      f"null={null_pct:4.1f}%  [{status}]  {date_range}")
            else:
                print(f"  {ticker:6s} {info['name']:28s} *** NOT FOUND ***")

        print(f"  → Found: {found_count}/{len(layer_dict)}")

    # Overall summary
    all_tickers_in_data = set(margin_df.index.get_level_values('Ticker').unique())
    total_found = len(all_tickers_in_data.intersection(set(TICKER_LIST)))
    total_obs = len(margin_df)
    print(f"\n{'=' * 70}")
    print(f"OVERALL: {total_found}/{len(TICKER_LIST)} tickers found, {total_obs} total observations")
    print(f"{'=' * 70}")


def ticker_summary_table(margin_df):
    """Summary table with layer assignments and key metrics."""
    print("\n" + "=" * 70)
    print("TICKER SUMMARY — Full Sample")
    print("=" * 70)

    rows = []
    for ticker in sorted(ALL_TICKERS.keys()):
        if ticker not in margin_df.index.get_level_values('Ticker'):
            continue

        info = ALL_TICKERS[ticker]
        td = margin_df.loc[ticker].sort_index()
        latest = td.iloc[-1]
        avg_gm = td['gross_margin'].mean()

        rows.append({
            'Ticker': ticker,
            'Name': info['name'],
            'Layer': info['layer'],
            'Envelope': info.get('envelope', '?'),
            'Mode': info.get('mode', '?'),
            'Quarters': len(td),
            'Avg GM': f"{avg_gm:.1%}",
            'Latest GM': f"{latest['gross_margin']:.1%}" if pd.notna(latest['gross_margin']) else 'N/A',
            'Rev $M': f"{latest['revenue'] / 1e6:.0f}" if pd.notna(latest['revenue']) else 'N/A',
        })

    summary = pd.DataFrame(rows)

    # Print by layer
    for layer in ['L1', 'L2', 'L3']:
        layer_df = summary[summary['Layer'] == layer]
        label = {'L1': 'Layer 1 (Deep)', 'L2': 'Layer 2 (Statistical)', 'L3': 'Layer 3 (Holdout)'}[layer]
        print(f"\n--- {label} ---")
        print(layer_df.to_string(index=False))

    # Envelope distribution
    print(f"\n--- Envelope Distribution ---")
    for env in ['T', 'M', 'L']:
        count = len(summary[summary['Envelope'] == env])
        label = {'T': 'Tight (<15%)', 'M': 'Moderate (15-30%)', 'L': 'Loose (>30%)'}[env]
        print(f"  {label}: {count} firms")

    print(f"\n  Total firms with data: {len(summary)}")

    return summary


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print("=" * 70)
    print("SUPPLY CHAIN CONSTRAINT SYSTEM — SimFin Data Pipeline v3")
    print(f"Expanded Sample: {len(ALL_TICKERS)} tickers across 3 layers")
    print("=" * 70)

    # Step 1: Load raw financial statements (direct CSV)
    print("\n--- Step 1: Loading financial statements ---")
    income_df = load_csv_direct('income')
    balance_df = load_csv_direct('balance')
    cashflow_df = load_csv_direct('cashflow')

    # Step 2: Construct framework variables
    print("\n--- Step 2: Constructing framework variables ---")
    margin_vars = construct_margin_variables(income_df)
    balance_vars = construct_balance_sheet_variables(balance_df)
    cashflow_vars = construct_cashflow_variables(cashflow_df)

    # Step 3: Rolling metrics (D5)
    print("\n--- Step 3: Rolling metrics ---")
    rolling_vars = construct_rolling_metrics(margin_vars)

    # Step 4: Cross-statement variables
    print("\n--- Step 4: Cross-statement derived variables ---")
    cross_vars = construct_cross_statement_variables(margin_vars, balance_vars, cashflow_vars)

    # Step 5: Quality report
    data_quality_report(margin_vars, balance_vars, cashflow_vars)
    summary = ticker_summary_table(margin_vars)

    # Step 6: Save everything
    print("\n--- Step 6: Saving processed data ---")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    saves = {
        'margin_variables.csv': margin_vars,
        'balance_sheet_variables.csv': balance_vars,
        'cashflow_variables.csv': cashflow_vars,
        'rolling_metrics.csv': rolling_vars,
        'cross_statement_variables.csv': cross_vars,
        'ticker_summary.csv': summary,
        'raw_income_statements.csv': income_df,
        'raw_balance_sheets.csv': balance_df,
        'raw_cashflow_statements.csv': cashflow_df,
    }

    for filename, df in saves.items():
        filepath = OUTPUT_DIR / filename
        df.to_csv(filepath)
        size_kb = filepath.stat().st_size / 1024
        print(f"  {filename} ({size_kb:.1f} KB)")

    # Save layer assignments as metadata
    import json
    meta = {
        'sample_design': {
            'layer_1': {t: {**v, 'layer': 'L1'} for t, v in LAYER_1.items()},
            'layer_2': {t: {**v, 'layer': 'L2'} for t, v in LAYER_2.items()},
            'layer_3': {t: {**v, 'layer': 'L3'} for t, v in LAYER_3.items()},
        },
        'total_tickers': len(ALL_TICKERS),
        'min_quarters': MIN_QUARTERS,
        'pipeline_version': 'v3',
    }
    meta_path = OUTPUT_DIR / 'sample_metadata.json'
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"  sample_metadata.json ({meta_path.stat().st_size / 1024:.1f} KB)")

    print(f"\n{'=' * 70}")
    print("PIPELINE v3 COMPLETE")
    print(f"{'=' * 70}")
    print(f"  Total tickers requested: {len(ALL_TICKERS)}")
    print(f"  Tickers with data: {margin_vars.index.get_level_values('Ticker').nunique()}")
    print(f"  Total observations: {len(margin_vars)}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Review ticker_summary.csv for any surprises")
    print(f"  2. Flag tickers with < {MIN_QUARTERS} quarters for potential exclusion")
    print(f"  3. Begin SEC EDGAR customer concentration extraction")
    print(f"  4. Construct network position variables (D1)")

    return margin_vars, balance_vars, cashflow_vars, rolling_vars, cross_vars


if __name__ == '__main__':
    main()
