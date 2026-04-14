# CLAUDE.md — Big Data Coursework

## Project Overview

Nepalese e-commerce sales analysis using **PySpark** (distributed data processing + MLlib).  
All heavy lifting runs on Spark; visualisation uses Matplotlib / Seaborn on collected Pandas frames.

---

## Directory Layout

```
BigDataCW/
├── Coursework_dataset/          # Raw CSVs (do not edit)
│   ├── customers.csv
│   ├── date_dim_helper.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── reviews.csv
│   └── suppliers.csv
│
├── cleaned_dataset/             # PySpark-output partitioned CSVs
│   ├── customers_cleaned.csv/
│   ├── date_dim_cleaned.csv/
│   ├── order_items_cleaned.csv/
│   ├── orders_cleaned.csv/
│   ├── products_cleaned.csv/
│   ├── reviews_cleaned.csv/
│   └── suppliers_cleaned.csv/
│
├── pyspark_cleaning/            # Data cleaning notebooks / scripts
├── non_pyspark_cleaning/        # Alternative cleaning scripts
│
├── sales_analysis.ipynb         # Business Insight 1: Sales Performance Analysis
├── sentiment_analysis.ipynb     # Business Insight 2: Sentiment Analysis on Reviews
│
├── CLAUDE.md                    # This file
└── README.md
```

---

## Notebooks

### `sales_analysis.ipynb` — Sales Performance Analysis

| Section | Topic |
|---------|-------|
| 0 | Setup & Spark session |
| 1 | Data loading (orders, order_items, products, customers, date_dim) |
| 2 | KPI dashboard — Revenue, Profit, Orders |
| 3 | Sales by product category |
| 4 | Sales by region (city-level) |
| 5 | Sales over time (yearly + monthly seasonality + heatmap) |
| 6 | Top-selling & low-performing products (Pareto) |
| 7 | Regression models (Linear Regression + Random Forest) to predict line_total |
| 8 | Key takeaways & next steps |

### `sentiment_analysis.ipynb` — Review Sentiment

Classifies product reviews (good / neutral / bad) using:
- PySpark MLlib **Logistic Regression** (TF-IDF features)
- HuggingFace **BERT** (transformer-based)

---

## Data Notes

- **Cleaned dataset** directories are Spark partition outputs — read with  
  `spark.read.csv("<path>", header=True, inferSchema=True)` (reads all part files).
- **Revenue proxy**: `line_total = quantity × unit_price_at_sale` (pre-computed in order_items).
- **Profit proxy**: `line_total × (1 − discount_pct) × 0.30` (30 % gross margin assumption).
- Only `order_status == "Delivered"` rows count towards confirmed revenue / profit KPIs.

---

## Coding Conventions

- **Always use PySpark** for data transformations and ML — no pandas on the raw Spark DataFrames.
- Collect to Pandas only for plotting (`df.toPandas()` after aggregation).
- Log-transform skewed regression targets (`F.log1p` / `F.expm1`) before fitting.
- Save every chart as a PNG (`plt.savefig(...)`) alongside displaying it.
- Use `spark.sparkContext.setLogLevel("ERROR")` to suppress INFO noise.
- Stop Spark at the end of each notebook: `spark.stop()`.

---

## Environment

- Python 3.10+
- PySpark 3.x (`local[*]`, 4 GB driver memory)
- Libraries: `pyspark`, `matplotlib`, `seaborn`, `pandas`, `numpy`, `scikit-learn`, `transformers`

---

## Key Business Insights Produced

1. **Sales Performance Analysis** (`sales_analysis.ipynb`)
   - Total revenue, profit, orders (KPI dashboard)
   - Revenue & profit by product category
   - Top 15 cities by revenue (bar + scatter)
   - Yearly trend & monthly seasonality (line, bar, heatmap)
   - Top 10 / Bottom 10 products + Pareto chart
   - Regression models: Linear Regression vs Random Forest for line_total prediction

2. **Sentiment Analysis** (`sentiment_analysis.ipynb`)
   - Review classification: good / neutral / bad
   - Logistic Regression (Spark MLlib) + BERT (HuggingFace)
