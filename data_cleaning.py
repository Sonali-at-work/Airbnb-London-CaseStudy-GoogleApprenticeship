import pandas as pd
import numpy as np
import re
import logging
class AirbnbDataCleaner:

    def __init__(self, df: pd.DataFrame):
        self.df = df


    def remove_duplicates(self):
        self.df = self.df.drop_duplicates(subset=["id", "quarter"])
        logging.info("Duplicates removed.")
        
    def clean_price(self):
        # Convert to numeric if price is in string format
        self.df["price"] = (
            self.df["price"].astype(str).str.replace(r"[^\d\.]", "", regex=True))   # remove $, commas, etc..replace("", np.nan).astype(float)
        
        self.df["price"] = pd.to_numeric(self.df["price"], errors="coerce")
        logging.info("Price cleaned.")

    def listing_status(self):
        self.df["listing_status"] = np.where(self.df["availability_365"] > 0,"Active","Inactive")
        logging.info("Listing status created.")

    def handle_missing_values(self):
        logging.info("Handling missing values...")

        print("Missing before imputation:")
        print(self.df[['bathrooms','beds','bedrooms']].isna().sum())
        cols = ['host_response_rate','host_identity_verified','host_is_superhost']
        # inputing values in cols
        self.df[cols] = (
        self.df[cols]
        .replace('N/A', 'unknown')   # replace string N/A
        .fillna('unknown')           # replace None/NaN
        )

        self.df['reviews_per_month'] = self.df['reviews_per_month'].fillna(0)

        self.df["bathrooms"] = pd.to_numeric(self.df["bathrooms"], errors="coerce")

        # Function to extract number of bathrooms from bathrooms_text
        def parse_bathrooms(text):
            if pd.isna(text):
                return np.nan

            s = str(text).lower()

            # captures numbers like "1", "1.5", "2.5"
            m = re.search(r'(\d+(\.\d+)?)', s)
            if m:
                 return float(m.group(1))

        # Apply parsing, but only fill where bathrooms is NaN
        mask_missing = self.df["bathrooms"].isna()
        self.df.loc[mask_missing, "bathrooms"] = (
        self.df.loc[mask_missing, "bathrooms_text"].apply(parse_bathrooms)
        )

        self.df['bathrooms'].fillna(
           self.df['bathrooms'].median(),
          inplace=True
          )
        self.df.drop('bathrooms_text',axis=1,inplace=True)

        self.df['beds'].fillna(self.df['beds'].median(),inplace =True)

        self.df['bedrooms'] = (self.df.groupby('property_type')['bedrooms'].transform(lambda x: x.fillna(x.median())))

    # logging.info("Imputing missing prices for active listings...")

        mask = (
               (self.df["listing_status"] == "Active") &
               (self.df["price"].isna())
               )

        group_median = (
                     self.df
                     .groupby(["neighbourhood_cleansed", "room_type"])["price"]
                    .transform("median")
                    )

        self.df.loc[mask, "price"] = group_median[mask]

        # logging.info("Price imputation completed.")

        logging.info("Missing value handling completed.")


    def create_features(self):
        logging.info("Creating occupancy and revenue features...")

        host_cols = ['host_since','host_response_time','host_identity_verified','host_acceptance_rate','host_response_rate','host_listings_count','host_total_listings_count']
        review_cols = ['review_scores_rating','review_scores_accuracy','review_scores_cleanliness','review_scores_checkin',
        'review_scores_communication','review_scores_location','review_scores_value','reviews_per_month','first_review','last_review']

        # Creating a Missing flag 
        self.df['host_info_missing_flag'] = (self.df[host_cols].isna().all(axis=1)).astype(int)

        self.df['no_reviews_flag'] = (self.df[review_cols].isna().all(axis=1)).astype(int)


        #  Creating a feature occ_rate_30 signifying the occupancy of active listings 
        mask = ((self.df["price"].notna()))
        # Occupancy proxy
        self.df.loc[mask, "occ_rate_30"] = ((1 - self.df.loc[mask, "availability_30"] / 30).clip(0, 1))

        # Quarterly revenue proxy (approx 90 days)
        self.df.loc[mask, "revenue_quarter"] = (self.df.loc[mask, "price"] *self.df.loc[mask, "occ_rate_30"] * 90)
    
        logging.info("Feature engineering completed")

