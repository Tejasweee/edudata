import pandas as pd

# Load the main file
df = pd.read_csv("bmgf_sectors.csv")
df = df[df['DIVISION'] != 'U.S. Program']

# Convert 'DATE COMMITTED' to year
df['DATE COMMITTED'] = pd.to_datetime(df['DATE COMMITTED'], errors='coerce').dt.year

# 1) global_sectors.csv: percentage of total overall (all sectors combined)
df1 = df.groupby('sector', as_index=False)['AMOUNT COMMITTED'].sum()
df1['percentage'] = (df1['AMOUNT COMMITTED'] / df1['AMOUNT COMMITTED'].sum() * 100).round(2)
df1 = df1.sort_values(by='AMOUNT COMMITTED', ascending=False)
df1.to_csv('global_sectors.csv', index=False)

# 2) global_sectors_year.csv: percentage of sector amount within each year
df2 = df.groupby(['sector', 'DATE COMMITTED'], as_index=False)['AMOUNT COMMITTED'].sum()
# Total per year (sum of amounts for all sectors in that year)
total_per_year = df2.groupby('DATE COMMITTED')['AMOUNT COMMITTED'].transform('sum')
df2['percentage'] = (df2['AMOUNT COMMITTED'] / total_per_year * 100).round(2)
df2 = df2.sort_values(by=['DATE COMMITTED', 'AMOUNT COMMITTED'], ascending=[True, False])
df2.to_csv('global_sectors_year.csv', index=False)

# 3) global_sectors_org.csv: percentage of amount within each sector (ignoring year)
df3 = df.groupby(['sector', 'GRANTEE'], as_index=False)['AMOUNT COMMITTED'].sum()
total_per_sector = df3.groupby('sector')['AMOUNT COMMITTED'].transform('sum')
df3['percentage'] = (df3['AMOUNT COMMITTED'] / total_per_sector * 100).round(2)
df3 = df3.sort_values(by='sector', ascending=True)  # Optionally sort by sector first
df3 = df3.sort_values(by='AMOUNT COMMITTED', ascending=False)
df3.to_csv('global_sectors_org.csv', index=False)

# 4) global_sectors_year_org.csv: percentage of amount per sector, per year
df4 = df.groupby(['sector', 'DATE COMMITTED', 'GRANTEE'], as_index=False)['AMOUNT COMMITTED'].sum()
# total amount per sector and year (sum of all grantees in that sector/year)
total_per_sector_year = df4.groupby(['sector', 'DATE COMMITTED'])['AMOUNT COMMITTED'].transform('sum')
df4['percentage'] = (df4['AMOUNT COMMITTED'] / total_per_sector_year * 100).round(2)
df4 = df4.sort_values(by=['DATE COMMITTED', 'AMOUNT COMMITTED'], ascending=[True, False])
df4.to_csv('global_sectors_year_org.csv', index=False)
