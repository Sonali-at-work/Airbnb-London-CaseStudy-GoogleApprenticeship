# Market Dynamics & Revenue Driver Analysis – London Airbnb

## Objective
Airbnb hosts in London face seasonal dips in occupancy and pricing, with limited visibility into which property types, neighborhoods, reviews, and superhost status drive bookings.  
This project analyzes London Airbnb listings to design KPIs and dashboards that enable data-driven decision-making.
The objective of this project is to analyze revenue performance and demand concentration across Airbnb listing segments defined by Room Type , Property Type, neighbourhood, quarter.

Using listing-level pricing and availability data, 

The goal of this analysis is to answer the following business questions:
### 1. Which Room Type × Property Type combinations perform the best?
- Identify top-performing listing configurations.
- Understand pricing trends across quarters.
- Determine whether revenue changes are driven more by pricing strategy or demand fluctuations.

### 2. Does occupancy directly drive revenue performance?
- Estimate occupancy using availability data.
- Analyze the relationship between occupancy and revenue.
- Understand whether higher occupancy consistently leads to stronger revenue.

### 3. How does revenue behave across quarters?
- Estimate quarterly revenue using price × occupancy proxy.
- Identify peak and weak demand cycles.
- Understand revenue seasonality for better forecasting and planning.
(Price reflects supply strategy, occupancy reflects demand — revenue captures the combined effect.)

### 4. Is revenue diversified or concentrated across room types?
-	Which room types generate the highest revenue while maintaining strong occupancy?
-	Is revenue spread across segments or concentrated in specific room types?
This helps:
-	Identify primary revenue drivers.
-	Guide investment and marketing allocation.
- Reduce dependency on limited segments.

### 5. Which exact listing configurations drive marketplace performance?
-	Analyze performance at a granular level (Room Type × Property Type).
-	Identify high-performing supply categories.
-	Support optimized host onboarding for specific property–room combinations.

### 6. Does revenue follow the 80/20 (Pareto) principle?
-	Check whether the top 20% of listing combinations generate ~80% of total revenue.
- Measure revenue concentration risk across segments.

### 7. Is marketplace performance geographically concentrated?
-	Which neighbourhoods drive the highest revenue and occupancy?
-	Are strong-performing areas limited to tourist-heavy zones?
This helps:
-	Identify areas with higher pricing power
-	Detect expansion opportunities in mid-tier neighbourhoods
-	Support strategic supply growth.

### 8. How do host characteristics impact revenue?
-	Analyze the impact of host response time and host experience on revenue.
-	Understand whether better host quality leads to higher monetization.
This supports:
-	Host acquisition strategy
-	Host retention focus
-	Marketplace quality improvement








## Dataset
- Source: Inside Airbnb dataset (publicly available).
- Size: ~500K listings (sample dataset included in `data/` folder for reproducibility).
- Key fields: price, availability, occupancy, property type, neighborhood, reviews, superhost status.
##  Repository Structure

```text
datasets/        → Source data
scripts/         → SQL scripts (ETL, modeling, QA)
docs/            → Architecture & data dictionary
tests/           → Data quality checks
README.md        → Project overview

data-warehouse-project/
│
├── datasets/
│   └── Raw datasets used for the project.
│
├── docs/
│   ├── Tables available and relationship between them.drawio
│   ├── output Screenshot of sql queries.drawio    # Draw.io file showing the project’s architecture
│   ├── data_catalog.md             # Catalog of datasets, including field descriptions and metadata
│   ├── data_flow.drawio            # Draw.io file for the data flow diagram
│   └── data_models.drawio          # Draw.io file for data models (Galaxy schema)
│
├── SQL scripts/
│   ├── Bronze- Raw data Loading/                        # Scripts for extracting and loading raw data/ Data Ingestion 
│   │    └── DDL_Script_Creating_Tables_and_Loading_Data
│   │
│   ├── Silver- Data Cleaning and Data Standardization/  # Scripts for cleaning and transforming data
│   │    ├──DDL_Script .sql
│   │    ├──Script_quality_checks_on_data .sql
│   │    ├──Stored Procedure for data Cleaning .sql
│   │    └──Tableas available and reationship between them .png
│   │
│   └── Gold- Data Modelling(Dimension and facts)/      # Scripts for creating analytical models
│        ├──Creating Fact and Dimension Tables .sql
│        ├──Quality checks on the data Model created
│        └──Schema.png
│
├── README.md                       # Project overview and instructions
├── LICENSE                         # License information for the repository
├── .gitignore                      # Files and directories to be ignored by Git
└── requirements.txt                # Dependencies and requirements for the project
```

#  Methodology

## 1️. Data Extraction

The dataset was extracted directly from **SQL Server** using `SQLAlchemy` and `pyodbc`.
A structured SQL query was used to create a consolidated `airbnb_summary` dataset containing listing-level, host-level, pricing, availability, and review attributes for all 4 quarters.

This help ensured:

* Centralized data logic
* Reproducibility
* Clean integration between SQL and Python analytics

## 2️. Data Cleaning & Missing Value Treatment

A structured missing value computation was performed:

* Computed NaN count and percentage of NaN per column.
* Identified columns with systematic missing patterns.

### Host Information Handling

* Verified that host-related attributes like host_since,host_response_time,host_response_rate,host_acceptance_rate,host_listings_count
,host_total_listings_count,host_identity_verified were missing together/ not randomly missing .
* Created:
  host_info_missing_flag to capture structurally incomplete host profiles.
* Standardized  columns -> 'host_since','host_acceptance_rate','host_response_rate','host_listings_count','host_total_listings_count' missing values as `"unknown"`

### Review Data Handling
* columns -> review_scores_accuracy,review_scores_cleanliness,review_scores_checkin,review_scores_communication,review_scores_location,review_scores_value
* Verified that review-related columns were missing together
* Created:
  "no_reviews_flag"
* Imputed `reviews_per_month` with 0 for listings with no reviews(NaN).

### Bathroom & Bedroom Cleaning
* Columns -> Beds, bathrooms,bathrooms_text, bedrooms
* Parsed numeric values from `bathrooms_text`
* Converted `bathrooms` to numeric
* Imputed NaN in: 
  * Bathrooms -> Median
  * Bedrooms -> Median within `property_type and bedroom`
* Dropped redundant `bathrooms_text` column

### column - Beds

* Imputed missing values in beds using median

### column Price Cleaning 
* Price is Not Missing at Random (NMAR)
* Removed currency symbols and commas
* Converted to numeric format
* Investigated missing price patterns relative to availability
   * **Combination_1** (Active lIstings) price = Nan ,has_availability = False ,and all availability_30,availability_60,availability_90,availability_365 as > 0 values
   * **Combination_2** (Blocked/Inactive) with Price= Nan ,has_availability = True ,and all availability_30,availability_60,availability_90,availability_365 as 0 values
   * **Combination_3** (Inactive) with price = NaN, has_availability = false , and all availability_30,availability_60,availability_90,availability_365 as 0
   * **Combination_4** (Unknown/Inactive) with price = NaN, has_availability = NaN, and all availability_30,availability_60,availability_90,availability_365 vary ( >0)
* **Impute Missing Prices for active listings or Combination 1** : Impute using  a hierarchy of medians:Group median by room_type  + neighbourhood_cleansed


### Creating column "listing_status"
* np.where(airbnb_summary["availability_365"] > 0,"Active","Inactive")
---

## 3. Feature Engineering

To support business analysis, several derived metrics were created.

### Occupancy Proxy (30-Day Window)

Since booking-level data was unavailable, availability was used as a demand proxy:

Occupancy Rate (30-day) = 1 − (availability_30 / 30)

Values were clipped between 0 and 1.
This acts as a demand intensity indicator.

### Revenue Proxy (Quarterly Estimate)

Revenue was approximated using:

Revenue Proxy (Quarterly) = price × occupancy_rate_30 × 90

This provides a standardized performance measure across listings.

## 4️. Active Listing Filtering each time we try to answer a business problem

Only active listings were retained:

* Non-null price
* Non-null availability_30

This ensures realistic revenue estimation.

---

## 5️. Plotting Histoograms ,box plot, countplot

<img src="SQL Scripts/Gold- Data Modelling (Dimensions and Facts)/Schema.png" width="600" height="500">


Listings were grouped by:

```
Room Type × Property Type
```

For each segment, the following KPIs were computed:

* Listings Count
* Median Occupancy
* Median Revenue (Quarterly)
* Total Revenue (Quarterly Proxy)

To reduce small-sample bias:

```
Minimum threshold: 100 listings per segment
```

---

## 6️⃣ Revenue Concentration Analysis

To evaluate portfolio dependency risk:

* Calculated Revenue Share %
* Sorted segments by Total Revenue
* Computed Cumulative Revenue %
* Built Pareto Visualization

This analysis identifies:

* High-revenue drivers
* Revenue concentration structure
* Long-tail performance segments
* Portfolio risk exposure

---

## 7️⃣ Visualization

Visualizations were created using:

* Matplotlib
* Seaborn

Key analytical outputs include:

* Distribution plots (beds, bathrooms, bedrooms)
* Segment performance charts
* Pareto chart for revenue concentration

---

# 🔎 Analytical Approach Summary

This project follows a structured analytics pipeline:

1. SQL Extraction
2. Data Auditing
3. Systematic Missing Treatment
4. Feature Engineering
5. Segment Aggregation
6. Revenue Concentration Modeling
7. Business Interpretation

The methodology focuses on balancing statistical rigor with business relevance.

---

If you'd like, I can now:

* Write your **Objective section** professionally
* Draft your **Key Insights section**
* Or restructure your entire README into a polished final version ready for GitHub** 🔥


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
- data/ # sample dataset
- notebooks 1/ Airbnb_1_EDA_&_Feature Engineering
- notebooks 2/ Airbnb_2_KPI_&_Hypothesis
- reports/ # summary visuals or dashboards
- README.md # project overview
- requirements.txt # dependencies

## Tools & Libraries
- Python (Pandas, NumPy, Matplotlib, Seaborn)
- Excel / Power Query (data cleaning, pivot dashboards)
- Power BI (optional dashboards)
