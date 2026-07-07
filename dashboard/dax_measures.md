# Power BI DAX Measures — Telco Customer Churn

This document provides production-ready DAX measures for the IBM Telco Customer Churn dataset. Use a table name of `CustomerChurn` (adjust if your model/table name differs).

Notes:
- Format percentage measures as Percentage (2 decimal places) in Power BI.
- Format money measures as Currency.
- Replace `CustomerChurn` with your actual table name if different.

---

## 1) Total Customers
Measure
```dax
Total Customers =
COUNTROWS( 'CustomerChurn' )
```
What it does
- Counts all rows (customers) in the `CustomerChurn` table.
Power BI visuals
- KPI card, Card visual, report header tiles.

---

## 2) Churned Customers
Measure
```dax
Churned Customers =
CALCULATE(
    COUNTROWS( 'CustomerChurn' ),
    'CustomerChurn'[Churn] = "Yes"
)
```
What it does
- Counts customers where the `Churn` column equals "Yes".
Power BI visuals
- Card visual, stacked bar (by segment), table.

---

## 3) Active Customers
Measure
```dax
Active Customers =
CALCULATE(
    COUNTROWS( 'CustomerChurn' ),
    'CustomerChurn'[Churn] = "No"
)
```
What it does
- Counts customers who have not churned (`Churn` = "No").
Power BI visuals
- Card visual, KPI, segmented bar.

---

## 4) Churn Rate
Measure
```dax
Churn Rate =
DIVIDE( [Churned Customers], [Total Customers], 0 )
```
What it does
- Calculates the proportion of customers who churned. `DIVIDE` avoids divide-by-zero errors.
Power BI visuals
- Card visual (format as %), line chart (trend over time if date dimension present), gauge.

---

## 5) Retention Rate
Measure
```dax
Retention Rate =
DIVIDE( [Active Customers], [Total Customers], 0 )
```
What it does
- Proportion of customers retained (non-churned).
Power BI visuals
- Card visual (format as %), trend chart, gauge.

---

## 6) Average Monthly Charges
Measure
```dax
Average Monthly Charges =
AVERAGE( 'CustomerChurn'[MonthlyCharges] )
```
What it does
- Computes the mean of the `MonthlyCharges` column.
Power BI visuals
- Card, boxplot (custom visual), column/line charts by segment.

---

## 7) Average Tenure
Measure
```dax
Average Tenure =
AVERAGE( 'CustomerChurn'[tenure] )
```
What it does
- Average customer tenure (in months).
Power BI visuals
- Card, histogram (custom visual or use bins), line chart by cohort.

---

## 8) Total Monthly Revenue
Measure
```dax
Total Monthly Revenue =
SUM( 'CustomerChurn'[MonthlyCharges] )
```
What it does
- Sums `MonthlyCharges` across all customers to estimate monthly recurring revenue.
Power BI visuals
- Card, stacked column by segment, area chart over time (if subscription date available).

---

## 9) Revenue Lost Due to Churn (Monthly)
Measure
```dax
Revenue Lost Due To Churn (Monthly) =
CALCULATE(
    SUM( 'CustomerChurn'[MonthlyCharges] ),
    'CustomerChurn'[Churn] = "Yes"
)
```
What it does
- Sums monthly charges for customers that have churned — an estimate of recurring monthly revenue exposed to churn.
Power BI visuals
- Card, stacked column by contract type or segment to show where revenue loss is concentrated.

---

## Formatting & Usage Tips
- Create the measures in the Modeling pane in Power BI Desktop.
- Use `Format` -> `Percentage` for `Churn Rate` and `Retention Rate` with 1–2 decimals.
- Use `Format` -> `Currency` for revenue measures and `Average Monthly Charges`.
- Use slicers for `Contract`, `InternetService`, `PaymentMethod`, and `tenure` cohorts to filter and compare measures.

## Optional derived measures (useful)
- Estimated Annual Revenue Lost
```dax
Estimated Annual Revenue Lost =
[Revenue Lost Due To Churn (Monthly)] * 12
```
- Churn Rate by Segment (example: Contract)
```dax
Churn Rate by Contract =
DIVIDE(
    CALCULATE( COUNTROWS('CustomerChurn'), 'CustomerChurn'[Churn] = "Yes" ),
    CALCULATE( COUNTROWS('CustomerChurn') ),
    0
)
```
(Use this measure placed in a matrix visual with `Contract` on rows.)

---

If you want, I can also:
- Generate a Power BI template (.pbit) with the data model and measures wired into a sample report.
- Create recommended visuals and layouts for an executive dashboard.

