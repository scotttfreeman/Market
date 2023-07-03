import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
df = pd.read_excel('spx_ew.xlsx', index_col=0)

# Sort the DataFrame in ascending order
df.sort_index(ascending=True, inplace=True)

def calculate_indexed_performance(df, target_dates, pre_days=90, post_days=365):
    # Create an empty DataFrame to store the indexed performances
    indexed_df = pd.DataFrame()
    
    for date in target_dates:
        # Select the 90 days before and 365 days after the date
        start = pd.to_datetime(date) - pd.DateOffset(days=pre_days)
        end = pd.to_datetime(date) + pd.DateOffset(days=post_days)
        sliced_df = df.loc[start:end, 'spx_ew']
        
        # Create new index representing days relative to the target date
        new_index = np.arange(-len(sliced_df.loc[:date]) + 1, len(sliced_df.loc[date:]) )
        sliced_df.index = new_index

        # Index to 100
        indexed_sliced_df = sliced_df / sliced_df.loc[0] * 100
        
        # Store the indexed performance in the data frame
        indexed_df = pd.concat([indexed_df, indexed_sliced_df], axis=1)
    
    # Name the columns after the target dates
    indexed_df.columns = target_dates
    
    return indexed_df

# List of dates to get indexed performance for
target_dates = ['1974-10-03', '1982-08-12', '1987-12-04', '1990-10-11', '1998-08-31', '2002-10-09', '2009-03-09', '2018-12-24', '2020-03-23', '2022-10-12']

indexed_df = calculate_indexed_performance(df, target_dates)
indexed_df['Average'] = np.mean(indexed_df.iloc[:,:-1],axis=1)
# indexed_df.to_excel('indexed_df.xlsx')

# Plotting indexed performance
plot_df = pd.concat([indexed_df['2022-10-12'], indexed_df['Average']], axis=1)
ax = plot_df.plot(kind='line', xlim=(-60, 250), xticks=range(-60, 360, 30))
lines = ax.get_lines() # customize line format
for line in lines:
    if line.get_label() == '2022-10-12':
        line.set_linewidth(2.5)
        line.set_color('#09A56C')
    if line.get_label() == 'Average':
        line.set_linewidth(2.5)
        line.set_color('#000000')

other_columns = indexed_df.columns[:-2]  # Plotting range excluding the last two columns (2022-10-12 and Average)

# Calculate the minimum and maximum values for each row in the other columns
min_values = indexed_df[other_columns].min(axis=1)
max_values = indexed_df[other_columns].max(axis=1)

ax.fill_between(indexed_df.index, min_values, max_values, alpha=0.3) # Fill between the minimum and maximum values
ax.axvline(x=0, color='black', linestyle='--') # Add a black dotted vertical line at the 0 x-axis value
ax.legend(['Current (since 10/12/22)', 'Historical Average', 'Historical Range', 'Market Bottom'])

plt.title('S&P Equal Weight Index Performance From Market Bottoms', fontweight='bold')
plt.xlabel('Days from Market Bottom')
plt.ylabel('Indexed to 100 (0 days = 100)')
plt.show()
