# Data Dictionary: Online Retail Dataset

This document defines the columns present in the [data.csv](file:///d:/Joshi/data.csv) dataset, including their data types, descriptions, and business relevance.

| Column Name | Data Type | Description | Business Relevance / Usage |
| :--- | :--- | :--- | :--- |
| **InvoiceNo** | Nominal / Object | A 6-digit unique identifier for each transaction. Invoices starting with the letter **'C'** denote cancellations. | Used to identify individual sales events and calculate order-level metrics (e.g. order count, average order value). Essential for filtering out cancellations. |
| **StockCode** | Nominal / Object | A 5-digit (or alphanumeric) unique identifier assigned to each product item. | Identifies specific products. Used for product popularity, affinity analysis, and inventory tracking. |
| **Description** | Nominal / Object | Text name/description of the product. | Provides human-readable information about items sold. Useful for text analytics and product category grouping. |
| **Quantity** | Quantitative / Integer | The quantity of each product item purchased per transaction. Negative values indicate returned or cancelled items. | Essential for calculating sales volume, unit sales, inventory demand, and processing transaction returns. |
| **InvoiceDate** | Temporal / Object | The date and time when the transaction was completed (typically formatted as MM/DD/YYYY HH:MM). | Enables chronological time-series analysis, tracking daily/monthly sales peaks, cohort analysis, and temporal buying patterns. |
| **UnitPrice** | Quantitative / Float | The price of a single unit of the product in British Pounds (£). | Critical for calculating total transaction revenue (`Quantity * UnitPrice`), pricing sensitivity, and revenue contributions. |
| **CustomerID** | Nominal / Float or Object | A 5-digit unique identifier assigned to each registered customer. | Crucial for customer-centric analysis (RFM segmentation, cohort retention, purchase frequency, and loyalty mapping). |
| **Country** | Nominal / Object | The country where the customer resides. | Enables geographic segmentation of customers, localized pricing strategies, and global sales distribution mapping. |