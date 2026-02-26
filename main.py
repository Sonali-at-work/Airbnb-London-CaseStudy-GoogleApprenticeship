"""
main.py

Purpose:
---------
This script serves as the orchestration layer of the London Airbnb Quarterly Analysis project. It coordinates the full ETL pipeline,
including data extraction, cleaning, feature engineering, and loading of the refined dataset back into SQL Server.

Pipeline Overview:
-------------------
1. Establish connection to SQL Server.
2. Execute a UNION query combining multiple quarterly listing tables.
3. Load raw data into a Pandas DataFrame.
4. Apply structured data cleaning and feature engineering using the AirbnbDataCleaner class.
5. Write the cleaned and enriched dataset back to the database for analytical and business intelligence use.

Key Design Principles:
-----------------------
- Separation of concerns (extraction, transformation, loading).
- Modular and reusable cleaning logic.
- Production-style pipeline structure.
- Logging enabled for traceability and monitoring.

This script represents a simplified production-style ETL workflow that prepares Airbnb listing data for downstream analytics,EDA, and business performance evaluation.

Author: Sonali Patel
Project: London Airbnb Quarterly Performance Analysis
"""
import logging
from sql_data_loader import SQLDataLoader
from data_cleaning import AirbnbDataCleaner

logging.basicConfig(level=logging.INFO)

def main():

    # 1.Create DB connection
    connection_string = "mssql+pyodbc://LAPTOP-TG4UPAEV\\SQLEXPRESS/London Airbnb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    loader = SQLDataLoader(connection_string)

    # 2️. Your UNION Query
    query = """
WITH airbnb_summary AS (

SELECT
id,listing_url,scrape_id,last_scraped,source,name,description,neighborhood_overview,picture_url,host_id,host_url,host_name,host_since,host_location,
host_about,host_response_time,host_response_rate,host_acceptance_rate,host_is_superhost,host_thumbnail_url,host_picture_url,host_neighbourhood,host_listings_count,
host_total_listings_count,host_verifications,host_has_profile_pic,host_identity_verified,neighbourhood,neighbourhood_cleansed,neighbourhood_group_cleansed,latitude,
longitude,property_type,room_type,accommodates,bathrooms,bathrooms_text,bedrooms,beds,price,minimum_nights,maximum_nights,
minimum_minimum_nights,maximum_minimum_nights,minimum_maximum_nights,maximum_maximum_nights,minimum_nights_avg_ntm,maximum_nights_avg_ntm,calendar_updated,
has_availability,availability_30,availability_60,availability_90,availability_365,calendar_last_scraped,number_of_reviews,number_of_reviews_ltm,
number_of_reviews_l30d,first_review,last_review,review_scores_rating,review_scores_accuracy,review_scores_cleanliness,review_scores_checkin,review_scores_communication,
review_scores_location,review_scores_value,license,instant_bookable,calculated_host_listings_count,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms,reviews_per_month,'2024Q3' AS quarter
FROM dbo.London_6_sep_2024_listings_final

UNION ALL

SELECT
id,listing_url,scrape_id,last_scraped,source,name,description,neighborhood_overview,picture_url,host_id,host_url,host_name,host_since,host_location,
host_about,host_response_time,host_response_rate,host_acceptance_rate,host_is_superhost,host_thumbnail_url,host_picture_url,host_neighbourhood,host_listings_count,
host_total_listings_count,host_verifications,host_has_profile_pic,host_identity_verified,neighbourhood,neighbourhood_cleansed,neighbourhood_group_cleansed,latitude,
longitude,property_type,room_type,accommodates,bathrooms,bathrooms_text,bedrooms,beds,price,minimum_nights,maximum_nights,
minimum_minimum_nights,maximum_minimum_nights,minimum_maximum_nights,maximum_maximum_nights,minimum_nights_avg_ntm,maximum_nights_avg_ntm,calendar_updated,
has_availability,availability_30,availability_60,availability_90,availability_365,calendar_last_scraped,number_of_reviews,number_of_reviews_ltm,
number_of_reviews_l30d,first_review,last_review,review_scores_rating,review_scores_accuracy,review_scores_cleanliness,review_scores_checkin,review_scores_communication,
review_scores_location,review_scores_value,license,instant_bookable,calculated_host_listings_count,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms,reviews_per_month,'2024Q4' AS quarter
FROM dbo.London_11_December_2024_listings_final

UNION ALL

SELECT
id,listing_url,scrape_id,last_scraped,source,name,description,neighborhood_overview,picture_url,host_id,host_url,host_name,host_since,host_location,
host_about,host_response_time,host_response_rate,host_acceptance_rate,host_is_superhost,host_thumbnail_url,host_picture_url,host_neighbourhood,host_listings_count,
host_total_listings_count,host_verifications,host_has_profile_pic,host_identity_verified,neighbourhood,neighbourhood_cleansed,neighbourhood_group_cleansed,latitude,
longitude,property_type,room_type,accommodates,bathrooms,bathrooms_text,bedrooms,beds,price,minimum_nights,maximum_nights,
minimum_minimum_nights,maximum_minimum_nights,minimum_maximum_nights,maximum_maximum_nights,minimum_nights_avg_ntm,maximum_nights_avg_ntm,calendar_updated,
has_availability,availability_30,availability_60,availability_90,availability_365,calendar_last_scraped,number_of_reviews,number_of_reviews_ltm,
number_of_reviews_l30d,first_review,last_review,review_scores_rating,review_scores_accuracy,review_scores_cleanliness,review_scores_checkin,review_scores_communication,
review_scores_location,review_scores_value,license,instant_bookable,calculated_host_listings_count,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms,reviews_per_month,'2025Q1' AS quarter
FROM dbo.London_4_March_2025_listings_final

UNION ALL

SELECT
id,listing_url,scrape_id,last_scraped,source,name,description,neighborhood_overview,picture_url,host_id,host_url,host_name,host_since,host_location,
host_about,host_response_time,host_response_rate,host_acceptance_rate,host_is_superhost,host_thumbnail_url,host_picture_url,host_neighbourhood,host_listings_count,
host_total_listings_count,host_verifications,host_has_profile_pic,host_identity_verified,neighbourhood,neighbourhood_cleansed,neighbourhood_group_cleansed,latitude,
longitude,property_type,room_type,accommodates,bathrooms,bathrooms_text,bedrooms,beds,price,minimum_nights,maximum_nights,
minimum_minimum_nights,maximum_minimum_nights,minimum_maximum_nights,maximum_maximum_nights,minimum_nights_avg_ntm,maximum_nights_avg_ntm,calendar_updated,
has_availability,availability_30,availability_60,availability_90,availability_365,calendar_last_scraped,number_of_reviews,number_of_reviews_ltm,
number_of_reviews_l30d,first_review,last_review,review_scores_rating,review_scores_accuracy,review_scores_cleanliness,review_scores_checkin,review_scores_communication,
review_scores_location,review_scores_value,license,instant_bookable,calculated_host_listings_count,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms,reviews_per_month,'2025Q2' AS quarter 
FROM dbo.London_10_June_2025_listings_final)

select 
id, host_id,host_since,host_response_time,host_response_rate,host_acceptance_rate,host_is_superhost,
host_listings_count,host_total_listings_count,host_identity_verified,neighbourhood_cleansed,latitude,
longitude,property_type,room_type,accommodates,bathrooms,bathrooms_text,bedrooms,beds,price,
minimum_nights,maximum_nights,maximum_maximum_nights,minimum_nights_avg_ntm,maximum_nights_avg_ntm,
has_availability,availability_30,availability_60,availability_90,availability_365,number_of_reviews,
number_of_reviews_ltm,number_of_reviews_l30d,first_review,last_review,review_scores_rating,review_scores_accuracy,
review_scores_cleanliness,review_scores_checkin,review_scores_communication,review_scores_location,
review_scores_value,calculated_host_listings_count,calculated_host_listings_count_entire_homes,
calculated_host_listings_count_private_rooms,calculated_host_listings_count_shared_rooms,reviews_per_month,quarter
from airbnb_summary
    """

    airbnb_summary = loader.fetch_data(query)

    # 3️. Run cleaning
    cleaner = AirbnbDataCleaner(airbnb_summary)
    cleaner.remove_duplicates()
    cleaner.clean_price()
    cleaner.listing_status()
    cleaner.handle_missing_values()
    cleaner.create_features()
    cleaned_df = cleaner.df
    # writing the dataset back to sql server for anlaysis .
    cleaned_df.to_sql(name="airbnb_listings_cleaned",con=loader.engine,if_exists="replace",index=False)  # or "append"
    logging.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()

