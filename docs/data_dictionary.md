# Data Dictionary

## orders.csv
order_id (unique key), order_date, customer_id, product_id, quantity, order_value, order_status, sales_channel.

## returns.csv
return_id (unique key), order_id (unique returned order), request_date, pickup_date, received_date, closed_date (blank for open), return_reason, return_status, return_channel, assigned_team, refund_amount (synthetic exposure), sla_days (5), processing_days (blank for open), sla_met (1/0), is_open (1/0).

## customers.csv
customer_id, customer_segment, region, city.

## products.csv
product_id, product_name, category.
