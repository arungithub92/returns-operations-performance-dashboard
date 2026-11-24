# Returns & Operations Performance Dashboard

Power BI, DAX, Power Query, SQL and Python portfolio project for analyzing e-commerce returns, reasons, refund exposure, SLA compliance, case aging and operational workload.

> All data is synthetic and generated for learning. It is not Flipkart or any real company's data.

## Business questions
1. What is the order volume and return rate?
2. Which categories and reasons drive returns?
3. What is the refund exposure?
4. What percentage of closed cases meet the five-day SLA?
5. How many cases are open and how old is the backlog?
6. Which teams and regions have the highest workload?
7. Which return reasons have longer processing times?

## Repository
- `data/`: orders, returns, customers and products CSVs
- `sql/`: MySQL schema and operational analysis queries
- `powerbi/`: DAX measures, Power Query guide and dashboard build guide
- `src/`: reproducible synthetic dataset generator
- `docs/`: data dictionary, metric definitions and dataset summary

## Dataset
10,000 orders, 800 customers, 20 products and return cases for a subset of orders. Order dates span 2025. Each returned order has one return case. The reporting snapshot date for open-case aging is 2025-12-31.

## Model
- customers[customer_id] 1:* orders[customer_id]
- products[product_id] 1:* orders[product_id]
- orders[order_id] 1:1 returns[order_id] (or 1:* if needed)
- Date[Date] 1:* orders[order_date] (active)
- Optional inactive Date-to-returns[request_date] relationship for request-date analysis.

## Dashboard pages
### 1. Executive Overview
Total orders, eligible orders, returned orders, return rate, open cases, SLA compliance, refund exposure, monthly trend and category/region return rates.
### 2. Returns Analysis
Return reasons, category/product returns, refund exposure, return channel and monthly return trends.
### 3. Operations & SLA
Open backlog by status, SLA performance, average processing days, case aging, team workload and open cases beyond SLA.

## Metric rules
- Eligible orders = Delivered + Returned; exclude Cancelled and In Transit.
- Return rate = returned orders / eligible orders.
- SLA compliance = closed/rejected cases within SLA / all closed/rejected cases. Open cases are not counted as SLA-compliant.
- Open backlog = records where `is_open = 1`.
- Refund exposure is a synthetic amount, not proof of a completed refund payment.
- Open case age uses the fixed 2025-12-31 snapshot.

## Getting started
1. Import the four CSVs into Power BI Desktop.
2. Apply types and cleanup described in `powerbi/power_query_m.md`.
3. Create relationships and add measures from `powerbi/dax_measures.dax`.
4. Follow `powerbi/dashboard_build_guide.md` to build three pages.
5. Run `sql/01_create_schema.sql`, load the CSVs into MySQL, and run `sql/02_operations_analysis.sql`.
6. Reconcile SQL and Power BI totals using the same metric definitions.

## Validation
Check unique order and return IDs, valid foreign keys, returned-order reconciliation, eligible-order denominator, closed-case SLA denominator, open-case aging and refund totals.

## Interview topics
Explain return-rate denominators, open vs closed SLA cases, case age vs processing duration, bottleneck analysis, SQL-to-Power-BI reconciliation and refund exposure vs completed refunds.

## Limitations
Synthetic dataset, one return case per returned order, and fixed snapshot date. Production extensions could add partial returns, return-line facts, status history, refund transactions, incremental refresh, RLS and scheduled refresh.
