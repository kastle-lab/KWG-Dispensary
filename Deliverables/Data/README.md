# Summary

This section contains PUMA-ACS-5-Year-Estinmates from the [U.S. Census Bureau](data.census.gov) (USCB).

# PUMA-ACS-5-Yr

The data in this section is calculated using the Housing Unit Weights as outlined by the USCB in the acs_pums_handbook located in this directory under the "Selecting Apporpriate Weights" section. It contains the following:

- Property Value
  - This data shows the median property value for housholds in each county of Ohio.
- Income-to-poverty Ratio
  - This data shows the number of households that fall into the low-income category by falling at or below 200% of the [federal poverty level in 2023](https://povertylevelcalculator.com/poverty-level-calculation-tables/#2023_Poverty_Level_Charts_In_Annual_Income).
- Household Income
  - This data shows the number of households that had a loss in 2023 or no income at all.

# ZCTA

This directory contains data about Ohio at the Zip Code Tabulated Areas (ZCTA) level in 2023 for the following:

- Household Income
- Demographics
- Housing Costs
- Health Insurance Coverage

# Life Expectancy

**NOTE**: Not all tract codes had life expectancy data.

The address of each dispensary was input into the [FFIEC geo map](https://geomap.ffiec.gov/ffiecgeomap/) where the tract codes (StateCode-CountyCode-TractCode) were taken and matched with the ohio-life-exp-census-2023 data.

# Voting Data

The 2020 voting data was extracted from the geojson file for each precinct in Ohio from [TheUpshot](https://github.com/TheUpshot/presidential-precinct-map-2020) repository. The coordinates of each dispensary were matched with their appropriate precincts, and the data were exported to a CSV file.
