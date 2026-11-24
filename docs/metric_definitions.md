# Metric Definitions

- Eligible Orders: Delivered + Returned orders; excludes Cancelled and In Transit.
- Returned Orders: distinct order IDs in returns.
- Return Rate: Returned Orders / Eligible Orders.
- Open Return Cases: is_open = 1.
- Closed Return Cases: is_open = 0 (Closed or Rejected).
- SLA Compliance: closed/rejected cases with sla_met = 1 / all closed/rejected cases.
- Open Cases Beyond SLA: open cases older than sla_days at snapshot date 2025-12-31.
- Average Processing Days: average populated processing_days.
- Refund Exposure: sum of synthetic refund_amount; not confirmed paid refunds.
- Open Case Age: snapshot date minus request_date for open cases.
