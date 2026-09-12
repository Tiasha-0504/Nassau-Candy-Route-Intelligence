# Nassau Candy Route Intelligence

## Factory-to-Customer Shipping Route Efficiency Analysis

An interactive Streamlit dashboard developed to analyze factory-to-customer shipping performance for Nassau Candy Distributor.

## Project Overview

This project evaluates shipping route performance by analyzing recorded shipment lead times, route volume, geographic patterns, potential bottlenecks, and shipping modes.

The dashboard is designed to support data-driven logistics analysis and identify consistently efficient routes and areas requiring further attention.

## Business Objectives

- Identify efficient factory-to-customer routes
- Identify routes with higher recorded lead times
- Compare shipping performance across regions and states
- Analyze geographic shipping bottlenecks
- Compare performance across shipping modes
- Provide detailed route-level shipment insights

## Dashboard Features

### Route Intelligence

- Factory-to-region route analysis
- Factory-to-state route analysis
- Average recorded lead time
- Lead-time variability
- Route efficiency benchmarking
- Top 10 and Bottom 10 route analysis
- Interactive route performance distribution

### Geographic View

- Regional shipping performance
- High-volume states
- Potential geographic bottleneck analysis
- Shipment volume vs. average lead-time analysis
- Interactive US shipping efficiency map
- Factory location visualization
- Map filters for factory, customer region, and analysis metric

### Ship Mode Analysis

- Average recorded lead time by ship mode
- Shipment volume by ship mode
- Lead-time variability by ship mode
- Standard vs. Expedited comparison
- Descriptive financial context

### Route Explorer

- Factory-to-state route selection
- Route shipment statistics
- Order-level shipment details
- Interactive Order Date → Ship Date timeline

### Interactive Filters

- Order date range
- Region
- State / Province
- Ship mode
- Lead-time threshold
- Map-specific factory filter
- Map-specific customer region filter
- Map metric selection

## Methodology

### Shipping Lead Time

Shipping Lead Time is calculated as:

`Ship Date - Order Date`

### Route Definition

A route is defined as:

`Factory + Customer Region`

or

`Factory + Customer State / Province`

### Route Metrics

Routes are evaluated using:

- Total shipments
- Average recorded lead time
- Lead-time variability

### Route Efficiency Score

A normalized 0–100 presentation score is used for factory-to-state routes. Higher scores represent better recorded route performance.

The score is an analytical presentation metric because the technical documentation specifies a normalized efficiency score but does not prescribe a specific normalization formula.

### Geographic Bottleneck Analysis

Potential geographic bottlenecks are identified using two conditions:

- Above-median shipment volume
- Above-median average recorded lead time

This provides a descriptive method for identifying states with relatively high shipment activity and higher recorded lead times.

## Data Validation

The dataset is validated for:

- Missing order dates
- Missing ship dates
- Invalid or negative lead times
- Geographic field consistency

Geographic fields are standardized by trimming whitespace.

Invalid or negative lead-time records are removed according to the documented validation methodology.

The underlying source values are not manually altered.

## Important Data Note

The recorded shipment dates in the source dataset result in multi-year calculated lead times.

The dashboard retains these recorded values rather than introducing an unsupported plausibility threshold or changing the source dates.

Therefore, lead-time and delay-related analysis refers specifically to the recorded shipment dates in the dataset.

## Ship Mode Definitions

### Standard

Standard Class

### Expedited

Same Day, First Class, and Second Class

The Standard vs. Expedited comparison is descriptive and uses recorded shipping lead time.

The dataset does not contain a dedicated shipping-cost field. Therefore, the Cost field is not interpreted as a shipping expense.

## Dashboard Controls

The dashboard provides interactive controls for:

- Order date range
- Customer region
- Customer state / province
- Ship mode
- Lead-time threshold
- Map factory
- Map customer region
- Map metric

These controls allow users to explore different segments of the shipment network without modifying the underlying source data.

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly

## Project Structure

Nassau-Candy-Route-Intelligence/
├── app.py
├── Nassau Candy Distributor.csv
├── requirements.txt
└── README.md

## How to Run Locally

### 1. Install the required packages

`pip install -r requirements.txt`

### 2. Run the Streamlit dashboard

`streamlit run app.py`

The dashboard will open in a local browser window.

## Project Deliverables

- Interactive Streamlit Dashboard
- Research Paper
- Executive Summary

## Project Purpose

The project demonstrates how data analysis and interactive visualization can be used to evaluate factory-to-customer shipping routes, identify geographic patterns, compare shipping modes, and support data-driven logistics decision-making.
