import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

gdpg = pd.read_csv(ROOT / "data" / "raw" / "gdp_growth" / "wb_gdp_pc.csv", skiprows=4)
le = pd.read_csv(ROOT / "data" / "raw" / "life_expectancy" / "wb_le.csv", skiprows=4)

# ---------------------------------------------------------------------------------------
# 1. Observe the GDP per capita growth dataframe
# 2. Clean GDP per capita growth dataframe
#   a. Drop useless columns and metadata
#   b. Drop rows that are not countries
#       i. Use metadata file for reference
#   c. Fill missing values
#       i. Check the time-series graph to analyze trend to determine fill value
# 3. Observe the life expectancy dataframe
# 4. Clean life expectancy dataframe
#   a. Drop useless columns and metadata
#   b. Drop rows that are not countries
#       i. Use metadata files for reference
#   c. Fill missing values
#       i. Check the time-series graph to analyze the trend to determine fill value
# 5. Merge GDP per capita growth and life expectancy dataframes
# 6. Analysis
# ---------------------------------------------------------------------------------------


# ---------------------------------------------
# 1. Observing GDP per Capita Growth DF
# ---------------------------------------------

# Structure
print(gdpg.head())
print(gdpg.shape)
print(gdpg.columns)
print(gdpg.info())

# Missing Values
print(gdpg.isna().sum().to_string())
print(gdpg.isna().sum().sum())
print(gdpg.isna().any(axis=1).sum())

# Notes:
# - Indicator Code should be dropped (metadata)
# - Indicator Name should be dropped (metadata)
# - 1960 Column should be dropped (all missing values)
# - Unnamed: 70 Column should be dropped (all missing values, metadata)
# - Removing rows with at least one missing value would reduce our sample size to zero
#   - Need to fill with a value

# ---------------------------------------------
# 2. Cleaning GDP per Capita Growth DF
# ---------------------------------------------

# Dropping Irrelevant Columns
gdpg = gdpg.drop(columns=["Indicator Code", "Indicator Code", "1960", "Unnamed: 70"])
print(gdpg)

fake_country_codes = [
    "ABW",
    "AFE",
    "AFW",
    "ARB",
    "ASM",
    "BMU",
    "CEB",
    "CHI",
    "CYM",
    "CUW",
    "EAP",
    "EAR",
    "EAS",
    "ECA",
    "ECS",
    "EMU",
    "EUU",
    "FRO",
    "GIB",
    "GRL",
    "GUM",
    "HKG",
    "IMN",
    "LAC",
    "LCN",
    "MAC",
    "MAF",
    "MEA",
    "MNA",
    "MNP",
    "NAC",
    "NCL",
    "PRI",
    "SAS",
    "SSA",
    "SSF",
    "SXM",
    "TCA",
    "TEA",
    "TEC",
    "TLA",
    "TMN",
    "TSA",
    "TSS",
    "VGB",
    "VIR",
    "WLD",
    "XKX",
    "CSS",
    "FCV",
    "HIC",
    "HPC",
    "IBD",
    "IBT",
    "IDA",
    "IDB",
    "IDX",
    "INX",
    "LDC",
    "LIC",
    "LMC",
    "LMY",
    "LTE",
    "MIC",
    "OED",
    "OSS",
    "PSS",
    "PRE",
    "PST",
    "SST",
    "UMC"
]

sov_gdpg = gdpg.copy()

for fake in fake_country_codes:
    sov_gdpg = sov_gdpg[sov_gdpg["Country Code"] != fake]

print(sov_gdpg)




