import pandas as pd
import numpy as np
from datetime import datetime
import os
from sklearn import metrics
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import pypyodbc
import numpy as np



folder_path = r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\Basic Listings"

def process_listings(csv_path):
    
    # Get Data
    df = pd.read_csv(csv_path)
    csv_date = os.path.basename(csv_path)[:-18]
    date = datetime.strptime(csv_date.replace('_', '/'), "%m/%d/%y")
    df = df.drop(['City.1'], axis=1)
    
    # Drop unnecessary columns
    listings = df.dropna(axis=1, how="all")
    cols_to_drop = [col for col, nunique in df.nunique().items() if nunique == 1]
    listings = listings.drop(columns=cols_to_drop, axis=1)
    listings.rename(columns={listings.columns[0]:"MLS"}, inplace=True)
    
    cols_to_drop = listings.columns[19:]
    listings = listings.drop(cols_to_drop, axis=1)
    
    # One hot encode
    listings = pd.get_dummies(listings, columns=['City'], prefix='', prefix_sep='')
    listings = pd.get_dummies(listings, columns=['Property Type'], prefix='', prefix_sep='')
    
    # Transform values
    listings['Square Footage'] = listings['Square Footage'].str.replace(",","")
    listings['Square Footage'] = listings['Square Footage'].str[:-5]
    listings['Lot Size'] = np.where(listings['Lot Size'].str.endswith("acres"),
                                               pd.to_numeric(listings['Lot Size'].str[:-5].str.replace(",","")) * 43560,
                                               listings['Lot Size'])
    listings['Lot Size'] = np.where(listings['Lot Size'].str.endswith("sqft"),
                                               pd.to_numeric(listings['Lot Size'].str[:-5].str.replace(",","")),
                                               listings['Lot Size'])
    listings['Lot Size'] = listings['Lot Size'].fillna(listings['Square Footage'])
    
    # Separate into the two dataframes
    prices = pd.DataFrame(listings[["MLS","Price"]]).copy()
    prices['Date'] = date
        
    houses = listings.drop(['Price'], axis=1)
        
    return prices, houses

def process_basic_listings(csv_path):
    
    # Get Data
    df = pd.read_csv(csv_path)
    csv_date = os.path.basename(csv_path)[:-4]
    date = datetime.strptime(csv_date.replace('_', '/'), "%m/%d/%y").date()
    
    # Drop unnecessary columns
    listings = df.dropna(axis=1, how="all")
    cols_to_drop = [col for col, nunique in df.nunique().items() if nunique == 1]
    listings = listings.drop(columns=cols_to_drop, axis=1)
    listings.rename(columns={listings.columns[0]:"MLS"}, inplace=True)
        
    # One hot encode
    listings['Cities'] = listings['City']
    listings = pd.get_dummies(listings, columns=['Cities'], prefix='', prefix_sep='')
    listings = pd.get_dummies(listings, columns=['Property Type'], prefix='', prefix_sep='')
    
    # Transform values
    listings['Square Footage'] = listings['Square Footage'].str.replace(",","")
    listings['Square Footage'] = listings['Square Footage'].str[:-5]
    listings['Lot Size'] = np.where(listings['Lot Size'].str.endswith("acres"),
                                               pd.to_numeric(listings['Lot Size'].str[:-5].str.replace(",","")) * 43560,
                                               listings['Lot Size'])
    listings['Lot Size'] = np.where(listings['Lot Size'].str.endswith("sqft"),
                                               pd.to_numeric(listings['Lot Size'].str[:-5].str.replace(",","")),
                                               listings['Lot Size'])
    
    listings['Lot Size'] = listings['Lot Size'].replace('- -', np.nan)
    
    listings['Lot Size'] = pd.to_numeric(listings['Lot Size'].fillna(listings['Square Footage']))
    
    listings['Price'] = pd.to_numeric(listings['Price'].str.replace("$","").str.replace(",",""))
    
    # Separate into the two dataframes
    prices = pd.DataFrame(listings[["MLS","Price"]]).copy()
    prices['Date'] = date
        
    houses = listings.drop(['Price', 'Price per/Sqft'], axis=1)
    
    houses.drop_duplicates(subset=['MLS'])
        
    return prices, houses

remodeled_dict = {
    
    }


if __name__ == "__main__":
    
    prices = []
    houses = []
    
    for file_path in os.listdir(folder_path):
        # if file_path[-8:-4] == "full":
        file_path = folder_path +"\\"+ file_path
        # p, h = process_listings(file_path)
        p, h = process_basic_listings(file_path)
        prices.append(p)
        houses.append(h)
    
    prices_df = pd.concat(prices)
    houses_df = pd.concat(houses)
    
    # Remove duplicate houses after concatenation    
    houses_df = houses_df.drop_duplicates(subset=['MLS'])
    
    prices_df.to_csv(r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\Processed Files\prices.csv", index=False)
    houses_df.to_csv(r"C:\Users\1461733766A\OneDrive - United States Air Force\Documents\Houses\Processed Files\houses.csv", index=False)
    