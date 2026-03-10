# Overview & Architecture
Project utilizing the ETL Process, using Python for data extraction from an API using requests, cleaning using the Pandas package, and loading to Snowflake. Data modeling was done in Snowflake and visualized in PowerBi. This project goes overs factors that possibly affect game ratings, including localizations, genre, and platform.

# Questions & Key Findings
### Questions this analysis aims to answer:
  1. Do games that release on more platforms have higher ratings?
  2. Are some platforms preferred over others?
  3. Does applying to other regions (via localization) affect game ratings?
  4. Is distribution a factor that plays in a game's rating?
  5. What platform has the most game releases?
  6. How have ratings changed over time?
  7. Are some genres preferred over others? Have ratings changed due to a change in preference?

### Key Findings
  1. All of the top highest performing genres along with the highest rated modern platforms are all between the range of 70-77. With no signifant peaks or outliers, we can infer that neither genre nor platform are factors that have a significant effect on game ratings.
  2. While Xbox as a platform family (which includes each generation of Xbox) has the highest rating, Nintendo and PC lead in volume of games peaking towards 2020 and then steadily declining.
  3. In the more recent years, PC has had more releases than any platform. Nintendo previously holds this most due to Nintendo's longevity over PC.
  4. All of the most leading games genres all have a general consensus on applying to strategy and problem solving.
  5. The scatter plot reveals that over time, game ratings have generally increased over the years. Since we've already established that the medium of platform or genre lead to marginal difference in rating variation, this fairly strong correlation could signify that game rating is more affected by increases in game quality rather than increases in game distribution.
  6. Games with localizations in Korea frequently have higher ratings on average. While this could be a matter of user preference in quality, another reasoning could be that higher quality games have localizations for these areas.

# Dashboard Preview
<img width="1317" height="745" alt="Updated Dashboard" src="https://github.com/user-attachments/assets/7202b9a4-6df3-48bc-87f8-ab80080b1fc2" />

# Limitations
- No Revenue Data
  - This analysis does not go into detail on the profit a game has generated, and thus is mainly focused on what affects game performance rather than game profit.
- No Budget Data
  - No budget data means that it cannot be analyzed from the perspective of game development, and statistics such as game rating and budget are not considered.
  - Other questions such as how video game budget affects the quality are also not considered and must be found elsewhere.

 # Tools Used
 1. Snowflake
 2. Python
 3. SQL
 4. Powerbi

# Sources
[IGDB Video Game Database](https://www.igdb.com/api)
