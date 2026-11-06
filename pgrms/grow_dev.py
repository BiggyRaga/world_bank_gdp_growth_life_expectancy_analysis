import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
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
# print(gdpg.head())
# print(gdpg.shape)
# print(gdpg.columns)
# print(gdpg.info())

# Missing Values
# print(gdpg.isna().sum().to_string())
# print(gdpg.isna().sum().sum())
# print(gdpg.isna().any(axis=1).sum())

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

sovereign_gdpg = gdpg.copy()

for fake in fake_country_codes:
    sovereign_gdpg = sovereign_gdpg[sovereign_gdpg["Country Code"] != fake]

year_cols = [c for c in sovereign_gdpg.columns if str(c).strip().isdigit()]
sovereign_gdpg["n_years"] = sovereign_gdpg[year_cols].count(axis=1)
sovereign_gdpg = sovereign_gdpg[sovereign_gdpg["n_years"] >= 30]
sovereign_gdpg["average_gdp_growth"] = sovereign_gdpg[year_cols].mean(axis=1)
sovereign_gdpg = sovereign_gdpg.drop(sovereign_gdpg.columns[2:-2], axis=1)
sovereign_gdpg = sovereign_gdpg.drop(columns=["n_years", "Country Code"])

# print(sovereign_gdpg)

# ---------------------------------------------
# 3. Observing Life Expectancy DF
# ---------------------------------------------

# Structure
# print(le.head())
# print(le.shape)
# print(le.columns)
# print(le.info())

# Missing Values
# print(le.isna().sum().to_string())
# print(le.isna().sum().sum())
# print(le.isna().any(axis=1).sum())

# Notes:
# - Need to drop columns:
#   - Country Code, after filteration
#   - Indicator Name
#   - Indicator Code
#   - Unnamed: 70
# - Need to filter for country codes of sovereign nations
# - Need to find nations with 30 or more non-null values

# ---------------------------------------------
# 4. Cleaning Life Expectancy DF
# ---------------------------------------------

sovereign_le = le.copy()

for fake in fake_country_codes:
    sovereign_le = sovereign_le[sovereign_le["Country Code"] != fake]

year_cols = [c for c in sovereign_le.columns if str(c).strip().isdigit()]
sovereign_le["n_years"] = sovereign_le[year_cols].count(axis=1)
sovereign_le = sovereign_le[sovereign_le["n_years"] >= 30]
sovereign_le["average_life_expectancy"] = sovereign_le[year_cols].mean(axis=1)
sovereign_le = sovereign_le.drop(sovereign_le.columns[2:-2], axis=1)
sovereign_le = sovereign_le.drop(columns=["n_years", "Country Code"])

# print(sovereign_le)

# ---------------------------------------------
# 5. Merge GDP growth and life expectancy DFs
# ---------------------------------------------

df_merge = pd.merge(sovereign_gdpg, sovereign_le, on="Country Name", how="inner")

print(df_merge)

# ---------------------------------------------
# 6. Linear Regression
# ---------------------------------------------

gdpg_le_fit = smf.ols("average_gdp_growth ~ average_life_expectancy", data=df_merge).fit()
print(gdpg_le_fit.summary())

intercept = gdpg_le_fit.params["Intercept"]
slope = gdpg_le_fit.params["average_life_expectancy"]

plt.scatter(x=df_merge["average_life_expectancy"], y=df_merge["average_gdp_growth"], alpha=0.5)

x_vals = df_merge["average_life_expectancy"]
y_vals = intercept + slope * x_vals

plt.plot(x_vals, y_vals, label=f"y = {slope:.2f}x + {intercept:.2f}")

plt.title("Average GDP per Capita Growth Rates by Average Life Expectancy among Sovereign Nations")
plt.ylabel("Average GDP per capita Growth Rates (%)")
plt.xlabel("Average Life Expectancy (Years)")
plt.legend()
plt.show()
