# GDP Growth and Life Expectancy

## Question
Is higher life expectancy associated with faster economic growth across countries?

## Data and method
World Bank data on annual GDP per capita growth and life expectancy. For each country, GDP per capita growth was averaged across available years, and life expectancy was averaged the same way. I ran a single OLS regression of average GDP growth on average life expectancy across 187 countries.

## Findings
- Each additional year of life expectancy is associated with about 0.0405 percentage points higher average annual GDP per capita growth (slope 0.0405, p = 0.001).
- The association is weak: R-squared is 0.060, so average life expectancy explains about 6 percent of the variation in average annual GDP per capita growth across countries.
- Intercept: -0.6549%
- This is an association, not evidence that longer lives directly cause faster growth.