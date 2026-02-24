# Market Dynamics & Revenue Driver Analysis – London Airbnb

## Objective
Airbnb hosts in London face seasonal dips in occupancy and pricing, with limited visibility into which property types, neighborhoods, reviews, and superhost status drive bookings.  
This project analyzes London Airbnb listings to design KPIs and dashboards that enable data-driven decision-making.
The objective of this project is to analyze revenue performance and demand concentration across Airbnb listing segments defined by Room Type , Property Type, neighbourhood, quarter.

Using listing-level pricing and availability data, the project aims to:

The goal of this analysis is to answer the following business questions:
### 1. Which Room Type × Property Type combinations perform the best?
•	Identify top-performing listing configurations.
•	Understand pricing trends across quarters.
•	Determine whether revenue changes are driven more by pricing strategy or demand fluctuations.


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
## Methodology


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
