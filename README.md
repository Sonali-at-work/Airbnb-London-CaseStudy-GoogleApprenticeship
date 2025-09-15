# Airbnb-London-CaseStudy-GoogleApprenticeship

## Objective
Airbnb hosts in London face seasonal dips in occupancy and pricing, with limited visibility into which property types, neighborhoods, reviews, and superhost status drive bookings.  
This project analyzes London Airbnb listings to design KPIs and dashboards that enable data-driven decision-making.

## Dataset
- Source: Inside Airbnb dataset (publicly available).
- Size: ~500K listings (sample dataset included in `data/` folder for reproducibility).
- Key fields: price, availability, occupancy, property type, neighborhood, reviews, superhost status.

## Methods
- **Data Cleaning** (Power Query, Pandas)
- **Missing Value Analysis**
- **Exploratory Data Analysis (EDA)**: distributions, correlations, seasonal trends
- **Feature Engineering**: occupancy rate, revenue proxy, active listings
- **KPI Design**: occupancy %, revenue proxy, seasonal trends, host performance

## Key Insights
- Occupancy shows **seasonal dips in Q1**, with recovery in summer (Q3).  
- **Property Type:** Entire homes/apartments dominate revenue; shared rooms underperform.  
- **Neighborhoods:** Central London areas (Westminster, Camden) lead in revenue, but some outer boroughs show stronger occupancy growth.  
- **Reviews & Ratings:** Superhost status and higher review scores correlate with significantly higher occupancy and pricing resilience.  
- Revenue proxy indicates strong demand concentration in ~20% of listings.  

## Project Structure
│── data/ # sample dataset
│── notebooks 1/ Airbnb_1_EDA_&_Feature Engineering
│── notebooks 2/ Airbnb_2_KPI_&_Hypothesis
│── reports/ # summary visuals or dashboards
│── README.md # project overview

│── requirements.txt # dependencies

## Tools & Libraries
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Excel / Power Query (data cleaning, pivot dashboards)
- Power BI (optional dashboards)
