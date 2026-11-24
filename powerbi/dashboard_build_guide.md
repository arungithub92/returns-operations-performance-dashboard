# Power BI Dashboard Build Guide

## Relationships
- customers[customer_id] 1:* orders[customer_id]
- products[product_id] 1:* orders[product_id]
- orders[order_id] 1:1 returns[order_id] (one return per returned order in this synthetic data)
- Date[Date] 1:* orders[order_date] active
- Optional inactive Date[Date] to returns[request_date] for request-date trend.

## Page 1 — Executive Overview
KPI cards: Total Orders, Eligible Orders, Returned Orders, Return Rate %, Open Cases, SLA Compliance %, Refund Exposure.
Charts: monthly orders/returns, return rate by category, returns by region.
Slicers: Date, Region, Category, Sales Channel.

## Page 2 — Returns Analysis
Return reasons bar chart; returns by category/product; refund exposure by reason; monthly return trend; return channel split; category/product matrix with eligible orders, returns and return rate.

## Page 3 — Operations & SLA
Open cases by status; SLA compliance; average processing days; cases beyond SLA; workload by assigned team; open case table with request date, case age, status, assigned team and SLA days.

## Business rules
SLA compliance denominator includes closed/rejected cases only. Open cases beyond SLA are separately shown as backlog risk. Refund exposure is not a completed refund payment amount. Use the fixed snapshot date 2025-12-31 for open-case age.

## Validation
Compare Power BI with SQL queries. Reconcile returned orders to return records, return-rate numerator/denominator, closed-case SLA numerator/denominator, open backlog, case age and refund exposure. Use identical filters in both tools.
