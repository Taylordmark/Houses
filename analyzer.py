# Analyze houses and prices dataframes


# Find first and final prices of houses df, set as values in houses df
# Get time on market from this data, set as new column in houses df


# Packages
import pandas as pd
import datetime
import numpy as np

def get_house_price_data(houses_df, prices_df):
    # For each house row, get all of the data where MLS ==\
    first_date = []
    last_date = []
    max_price = []
    min_price = []
    time_on_market = []
    
    for index, row in houses_df.iterrows():
        # Get initial date, final date, max price, min price
        related_prices = prices_df[prices_df["MLS"] == row["MLS"]]
        
        min_d, max_d = pd.to_datetime(related_prices["Date"]).agg(['min', 'max'])
        min_p, max_p = related_prices['Price'].agg(['min','max'])
        
        first_date.append(min_d.date())
        last_date.append(max_d.date())
        max_price.append(max_p)
        min_price.append(min_p)
        time_on_market.append((max_d - min_d).days)
        
        
    houses_df['first_date'] = first_date
    houses_df['last_date'] = last_date
    houses_df['max_price'] = max_price
    houses_df['min_price'] = min_price
    houses_df['market_time'] = time_on_market
    
    # Fill NA values (for cities from get dummies) with False boolean
    houses_df.fillna(False, inplace=True)
    
    return(houses_df)

def add_location(house_prices, locations_df):
    
    houses = house_prices.merge(locations_df, on="MLS", how='left', suffixes=('', '_2'))
    houses.drop(houses.filter(regex='2$').columns, axis=1, inplace=True)
    houses.drop(houses.filter(regex='1$').columns, axis=1, inplace=True)
    
    cols_to_drop = [col for col, nunique in houses.nunique().items() if nunique == 1]
    cols_to_drop = cols_to_drop + ["Accuracy Score", "Street", "Unit Type","Unit Number","Number"]
    houses = houses.drop(columns=cols_to_drop, axis=1)
    
    return houses

if __name__ == '__main__':
    houses_loc = r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\Processed Files\houses.csv"
    prices_loc = r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\Processed Files\prices.csv"
    locations_loc = r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\geocod.csv"
    
    houses_df = pd.read_csv(houses_loc)
    prices_df = pd.read_csv(prices_loc)
    locations_df = pd.read_csv(locations_loc)
    
    house_prices = get_house_price_data(houses_df, prices_df)
    
    houses = add_location(house_prices, locations_df)

    print(houses_df)
    
    
# Then analyze price based on these factors


# Do something with roommate dataframe for price estimate based on description, location... ??


# Add another row for whether the house has a loft?
# Maybe, but this may be encompassed by KNN or somethign similar
