"""
SimFin Universe Discovery — Supply Chain Constraint System
==========================================================
Identifies all automotive-related companies in SimFin's free US dataset.
Determines the realistic sample universe for the pilot study.

Usage:
    python src/data_collection/simfin_discovery.py

Requires:
    - .env file with SIMFIN_API_KEY=your_key
    - pip install simfin pandas python-dotenv
"""

import os
import simfin as sf
import pandas as pd
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

sf.set_api_key(api_key=API_KEY)
sf.set_data_dir(str(SIMFIN_DATA_DIR))

# Automotive-related SIC codes and SimFin industry IDs
# We cast a wide net, then filter
AUTO_KEYWORDS = [
    'auto', 'vehicle', 'motor', 'automotive', 'car ', 'truck',
    'drivetrain', 'powertrain', 'brake', 'steering', 'suspension',
    'exhaust', 'transmission', 'axle', 'engine', 'seat',
    'tier 1', 'tier 2', 'oem', 'parts', 'component',
    'electrical equipment', 'electronic components',
    'thermal', 'lighting', 'glass', 'rubber', 'plastic',
]

# SIC codes relevant to auto supply chain
# 3714 = Motor Vehicle Parts & Accessories (primary)
# 3711 = Motor Vehicles & Car Bodies (OEMs — for reference, not in sample)
# 3713 = Truck & Bus Bodies
# 3592 = Carburetors, Pistons, Rings, Valves
# 3559 = Special Industry Machinery (some auto equipment)
# 3679 = Electronic Components NEC
# 3694 = Electrical Equipment for Internal Combustion Engines
# 3647 = Vehicular Lighting Equipment
# 3585 = Heating/AC Equipment (thermal management)
# 3562 = Ball & Roller Bearings
# 3599 = Industrial Machinery NEC
# 3089 = Plastics Products NEC
# 3061 = Molded Rubber Products
AUTO_SIC_CODES = [
    3714, 3711, 3713, 3592, 3559, 3679, 3694, 3647,
    3585, 3562, 3599, 3089, 3061, 3312, 3316, 3317,
    3462, 3463, 3465, 3469, 3499, 3511, 3519, 3568,
    3613, 3621, 3625, 3669, 3678, 3699, 3812, 3825,
]


# ============================================================
# STEP 1: Load company list from SimFin
# ============================================================

def load_companies():
    """Download and read the SimFin companies list, bypassing sf.load_companies()."""
    print("=" * 70)
    print("STEP 1: Loading SimFin company universe")
    print("=" * 70)

    # Try to trigger download
    companies_file = SIMFIN_DATA_DIR / 'us-companies.csv'
    if not companies_file.exists():
        print("  Downloading company list...")
        try:
            sf.load_companies(market='us')
        except TypeError:
            pass  # Expected — date_parser bug
        except Exception as e:
            print(f"  Download triggered with error: {e}")

    if not companies_file.exists():
        # Try alternate filename
        for f in SIMFIN_DATA_DIR.iterdir():
            if 'companies' in f.name.lower() and f.suffix == '.csv':
                companies_file = f
                break

    if not companies_file.exists():
        raise FileNotFoundError(
            f"Cannot find companies file in {SIMFIN_DATA_DIR}. "
            "Check SimFin data directory for available files."
        )

    print(f"  Reading {companies_file.name}...")
    df = pd.read_csv(companies_file, sep=';')
    print(f"  Total companies in SimFin US dataset: {len(df)}")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  First 5 rows:")
    print(df.head().to_string())
    return df


# ============================================================
# STEP 2: Load industries list
# ============================================================

def load_industries():
    """Download and read SimFin industries list."""
    print("\n" + "=" * 70)
    print("STEP 2: Loading SimFin industry classifications")
    print("=" * 70)

    industries_file = SIMFIN_DATA_DIR / 'us-industries.csv'

    # Check for any industries file
    if not industries_file.exists():
        for f in SIMFIN_DATA_DIR.iterdir():
            if 'industr' in f.name.lower() and f.suffix == '.csv':
                industries_file = f
                break

    # Try downloading via SimFin
    if not industries_file.exists():
        print("  Downloading industries list...")
        try:
            sf.load_industries()
        except TypeError:
            pass
        except Exception as e:
            print(f"  Download triggered with error: {e}")

    # Check again after download attempt
    if not industries_file.exists():
        for f in SIMFIN_DATA_DIR.iterdir():
            if 'industr' in f.name.lower() and f.suffix == '.csv':
                industries_file = f
                break

    if industries_file.exists():
        print(f"  Reading {industries_file.name}...")
        df = pd.read_csv(industries_file, sep=';')
        print(f"  Total industries: {len(df)}")
        print(f"  Columns: {list(df.columns)}")
        print(f"\n  All industries:")
        print(df.to_string())
        return df
    else:
        print("  WARNING: No industries file found. Will use company data only.")
        print(f"  Files in {SIMFIN_DATA_DIR}:")
        for f in sorted(SIMFIN_DATA_DIR.iterdir()):
            print(f"    {f.name} ({f.stat().st_size / 1024:.1f} KB)")
        return None


# ============================================================
# STEP 3: Identify automotive-related companies
# ============================================================

def find_auto_companies(companies_df, industries_df=None):
    """Find all companies that could be automotive suppliers."""
    print("\n" + "=" * 70)
    print("STEP 3: Identifying automotive-related companies")
    print("=" * 70)

    results = []

    # Method 1: Search by industry classification if available
    if industries_df is not None and 'IndustryId' in companies_df.columns:
        # Find auto-related industry IDs
        auto_industries = industries_df[
            industries_df.apply(
                lambda row: any(
                    kw in str(row).lower() for kw in AUTO_KEYWORDS
                ), axis=1
            )
        ]
        if len(auto_industries) > 0:
            print(f"\n  Auto-related industries found:")
            print(auto_industries.to_string())
            auto_industry_ids = auto_industries.iloc[:, 0].tolist()  # First column is usually ID
            industry_matches = companies_df[companies_df['IndustryId'].isin(auto_industry_ids)]
            print(f"\n  Companies matching auto industry IDs: {len(industry_matches)}")
            results.append(('industry_match', industry_matches))

    # Method 2: Search company names for auto keywords
    name_col = None
    for col in ['Company Name', 'Company', 'Name', 'name']:
        if col in companies_df.columns:
            name_col = col
            break

    if name_col:
        name_matches = companies_df[
            companies_df[name_col].str.lower().str.contains(
                '|'.join(['auto', 'vehicle', 'motor', 'brake', 'axle',
                          'steering', 'transmission', 'powertrain', 'seat',
                          'exhaust', 'engine', 'drivetrain', 'thermal']),
                na=False
            )
        ]
        print(f"\n  Companies matching auto keywords in name: {len(name_matches)}")
        if len(name_matches) > 0:
            print(name_matches.to_string())
        results.append(('name_match', name_matches))

    return results


# ============================================================
# STEP 4: Check which companies have financial data
# ============================================================

def check_data_availability(companies_df):
    """
    Cross-reference company list against the income statement data
    we already downloaded to see who has actual financial data.
    """
    print("\n" + "=" * 70)
    print("STEP 4: Checking financial data availability")
    print("=" * 70)

    income_file = SIMFIN_DATA_DIR / 'us-income-quarterly.csv'
    if not income_file.exists():
        print("  Income statement file not found. Run simfin_pipeline.py first.")
        return None

    print("  Reading income statement file to extract all available tickers...")
    # Just read the Ticker column to save memory
    income_df = pd.read_csv(income_file, sep=';', usecols=['Ticker'])
    available_tickers = set(income_df['Ticker'].unique())
    print(f"  Total tickers with quarterly income data: {len(available_tickers)}")

    # Find which company list tickers have data
    ticker_col = None
    for col in ['Ticker', 'ticker', 'TICKER']:
        if col in companies_df.columns:
            ticker_col = col
            break

    if ticker_col:
        companies_with_data = companies_df[companies_df[ticker_col].isin(available_tickers)]
        print(f"  Companies in company list WITH income data: {len(companies_with_data)}")
        companies_without_data = companies_df[~companies_df[ticker_col].isin(available_tickers)]
        print(f"  Companies in company list WITHOUT income data: {len(companies_without_data)}")
        return available_tickers
    else:
        print(f"  Could not find Ticker column. Available columns: {list(companies_df.columns)}")
        return available_tickers


# ============================================================
# STEP 5: Full universe scan of income data
# ============================================================

def scan_full_income_universe():
    """
    Read all tickers from the income statement file and count
    how many quarters each has. This gives us the true universe.
    """
    print("\n" + "=" * 70)
    print("STEP 5: Full universe scan — all tickers with financial data")
    print("=" * 70)

    income_file = SIMFIN_DATA_DIR / 'us-income-quarterly.csv'
    if not income_file.exists():
        print("  Income file not found.")
        return None

    print("  Scanning full income statement dataset...")
    df = pd.read_csv(income_file, sep=';', usecols=['Ticker', 'Report Date', 'Revenue', 'Gross Profit'])

    # Count quarters per ticker
    ticker_counts = df.groupby('Ticker').agg(
        quarters=('Report Date', 'count'),
        min_date=('Report Date', 'min'),
        max_date=('Report Date', 'max'),
        avg_revenue=('Revenue', 'mean'),
        avg_gross_profit=('Gross Profit', 'mean'),
    ).reset_index()

    # Calculate average gross margin
    ticker_counts['avg_gm'] = ticker_counts['avg_gross_profit'] / ticker_counts['avg_revenue']

    # Sort by quarters available (descending)
    ticker_counts = ticker_counts.sort_values('quarters', ascending=False)

    print(f"\n  Total unique tickers with income data: {len(ticker_counts)}")
    print(f"  Tickers with 10+ quarters: {len(ticker_counts[ticker_counts['quarters'] >= 10])}")
    print(f"  Tickers with 15+ quarters: {len(ticker_counts[ticker_counts['quarters'] >= 15])}")
    print(f"  Tickers with 19 quarters (full panel): {len(ticker_counts[ticker_counts['quarters'] >= 19])}")

    # Distribution of quarter counts
    print(f"\n  Quarter count distribution:")
    for q in [1, 5, 10, 15, 19, 20]:
        count = len(ticker_counts[ticker_counts['quarters'] >= q])
        print(f"    >= {q:2d} quarters: {count:4d} tickers")

    return ticker_counts


# ============================================================
# STEP 6: Known automotive tickers check
# ============================================================

def check_known_auto_tickers(available_tickers_df):
    """
    Check a curated list of known automotive suppliers
    against the SimFin data to see who's available.
    """
    print("\n" + "=" * 70)
    print("STEP 6: Checking known automotive supplier tickers")
    print("=" * 70)

    # Comprehensive list of publicly traded auto suppliers
    known_auto = {
        # === Your current 10 ===
        'GNTX': 'Gentex Corp',
        'DAN':  'Dana Inc',
        'AXL':  'American Axle',
        'LEA':  'Lear Corp',
        'ADNT': 'Adient',
        'MOD':  'Modine Manufacturing',
        'VC':   'Visteon',
        'APTV': 'Aptiv',
        'THRM': 'Gentherm',
        'SRI':  'Stoneridge',

        # === Large Tier 1 ===
        'MGA':  'Magna International',
        'BWA':  'BorgWarner',
        'ALV':  'Autoliv',
        'ALSN': 'Allison Transmission',
        'DORM': 'Dorman Products',
        'CWH':  'Camping World (aftermarket)',
        'FOXF': 'Fox Factory',
        'GTX':  'Garrett Motion',
        'MNRO': 'Monro Inc (aftermarket)',
        'MTOR': 'Meritor (now Cummins)',
        'NN':   'NN Inc',
        'PHIN': 'PHINIA Inc',
        'SMP':  'Standard Motor Products',
        'SUP':  'Superior Industries',
        'TEN':  'Tenneco (pre-Apollo)',
        'TOWR': 'Tower Semiconductor',
        'WBC':  'WABCO (pre-ZF)',

        # === Tier 1-2 Specialists ===
        'ALGN': 'Align Technology',
        'AOS':  'A.O. Smith',
        'ARNC': 'Arconic',
        'CPS':  'Cooper-Standard',
        'CTB':  'Cooper Tire (pre-Goodyear)',
        'DLPH': 'Delphi Technologies',
        'DY':   'Dycom Industries',
        'FLEX': 'Flex Ltd (contract mfg)',
        'GPC':  'Genuine Parts Co',
        'GT':   'Goodyear Tire',
        'HAR':  'Harman International',
        'HI':   'Hillenbrand',
        'HNST': 'Honest Company',
        'ITT':  'ITT Inc',
        'LKQ':  'LKQ Corp (aftermarket)',
        'LCII': 'LCI Industries',
        'MASI': 'Masimo Corp',
        'MPAA': 'Motorcar Parts of America',
        'SHLO': 'Shiloh Industries',
        'SNA':  'Snap-on',
        'TTC':  'Toro Company',
        'WGO':  'Winnebago',

        # === Electrical/Electronics for vehicles ===
        'AMZN': 'skip',  # Not auto
        'AEIS': 'Advanced Energy Industries',
        'BDC':  'Belden Inc',
        'CUI':  'CUI Global',
        'LFUS': 'Littelfuse',
        'MEI':  'Methode Electronics',
        'NXPI': 'NXP Semiconductors',
        'ON':   'ON Semiconductor',
        'ST':   'Sensata Technologies',
        'TEL':  'TE Connectivity',
        'VNET': 'Vnet Group',

        # === Diversified Industrials with auto exposure ===
        'CMI':  'Cummins',
        'DOV':  'Dover Corp',
        'EMR':  'Emerson Electric',
        'ETN':  'Eaton Corp',
        'HON':  'Honeywell',
        'IEX':  'IDEX Corp',
        'PH':   'Parker Hannifin',
        'ROK':  'Rockwell Automation',
        'ROP':  'Roper Technologies',
        'TXT':  'Textron',

        # === Materials/Chemical suppliers to auto ===
        'APD':  'Air Products',
        'CE':   'Celanese',
        'DD':   'DuPont',
        'DOW':  'Dow Inc',
        'EMN':  'Eastman Chemical',
        'HUN':  'Huntsman Corp',
        'PPG':  'PPG Industries',
        'RPM':  'RPM International',
        'TROX': 'Tronox',
    }

    if available_tickers_df is None:
        print("  No ticker data available for comparison.")
        return

    available_set = set(available_tickers_df['Ticker'].values)

    found = []
    not_found = []

    for ticker, name in sorted(known_auto.items()):
        if name == 'skip':
            continue
        if ticker in available_set:
            row = available_tickers_df[available_tickers_df['Ticker'] == ticker].iloc[0]
            found.append({
                'Ticker': ticker,
                'Name': name,
                'Quarters': int(row['quarters']),
                'From': row['min_date'],
                'To': row['max_date'],
                'Avg Revenue ($M)': f"{row['avg_revenue'] / 1e6:.0f}" if pd.notna(row['avg_revenue']) else 'N/A',
                'Avg GM': f"{row['avg_gm']:.1%}" if pd.notna(row['avg_gm']) else 'N/A',
            })
        else:
            not_found.append({'Ticker': ticker, 'Name': name})

    print(f"\n  FOUND in SimFin ({len(found)} tickers):")
    if found:
        found_df = pd.DataFrame(found)
        found_df = found_df.sort_values('Quarters', ascending=False)
        print(found_df.to_string(index=False))

    print(f"\n  NOT FOUND in SimFin ({len(not_found)} tickers):")
    if not_found:
        not_found_df = pd.DataFrame(not_found)
        print(not_found_df.to_string(index=False))

    # Summary by GM range (helps with taxonomy classification)
    if found:
        found_df_numeric = pd.DataFrame(found)
        print(f"\n  --- Distribution by Avg Gross Margin ---")
        print(f"  This helps classify firms by constraint envelope tightness:")
        gm_vals = []
        for f in found:
            try:
                gm = float(f['Avg GM'].strip('%')) / 100
                gm_vals.append((f['Ticker'], f['Name'], gm))
            except:
                pass

        gm_vals.sort(key=lambda x: x[2])
        for ticker, name, gm in gm_vals:
            envelope = 'Tight' if gm < 0.15 else ('Moderate' if gm < 0.30 else 'Loose')
            bar = '#' * int(gm * 100)
            print(f"    {ticker:6s} {name:30s} {gm:6.1%}  [{envelope:8s}]  {bar}")

    return found, not_found


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("SIMFIN UNIVERSE DISCOVERY")
    print("Supply Chain Constraint System — Sample Universe Analysis")
    print("=" * 70)

    # Step 1: Load companies
    try:
        companies_df = load_companies()
    except Exception as e:
        print(f"  Could not load companies: {e}")
        companies_df = None

    # Step 2: Load industries
    industries_df = load_industries()

    # Step 3: Find auto companies by name/industry
    if companies_df is not None:
        find_auto_companies(companies_df, industries_df)

    # Step 4: Check data availability
    if companies_df is not None:
        check_data_availability(companies_df)

    # Step 5: Full universe scan
    ticker_universe = scan_full_income_universe()

    # Step 6: Check known auto tickers
    if ticker_universe is not None:
        found, not_found = check_known_auto_tickers(ticker_universe)

    print("\n" + "=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review the found tickers and select your 60-90 firm sample")
    print("  2. Classify each firm using the three-axis taxonomy (P/C/E, T/M/L, H/M/L)")
    print("  3. Assign to Layer 1 (deep analysis), Layer 2 (statistical), or Layer 3 (holdout)")
    print("  4. Update simfin_pipeline.py with the expanded ticker list")


if __name__ == '__main__':
    main()
