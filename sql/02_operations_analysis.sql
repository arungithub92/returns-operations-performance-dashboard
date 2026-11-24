USE returns_operations;
-- 1. Executive return rate
SELECT COUNT(*) total_orders,
 SUM(order_status='Returned') returned_orders,
 ROUND(100*SUM(order_status='Returned')/NULLIF(SUM(order_status IN ('Delivered','Returned')),0),2) return_rate_pct
FROM orders;
-- 2. Return reasons and refund exposure
SELECT return_reason,COUNT(*) cases,ROUND(SUM(refund_amount),2) refund_exposure FROM returns GROUP BY return_reason ORDER BY cases DESC;
-- 3. Category return rate
SELECT p.category,COUNT(DISTINCT o.order_id) eligible_orders,COUNT(DISTINCT r.return_id) returns,
 ROUND(100*COUNT(DISTINCT r.return_id)/NULLIF(COUNT(DISTINCT o.order_id),0),2) return_rate_pct
FROM orders o JOIN products p ON p.product_id=o.product_id
LEFT JOIN returns r ON r.order_id=o.order_id
WHERE o.order_status IN ('Delivered','Returned') GROUP BY p.category ORDER BY return_rate_pct DESC;
-- 4. SLA compliance for closed/rejected cases only
SELECT COUNT(*) closed_cases,SUM(sla_met=1) within_sla,
 ROUND(100*SUM(sla_met=1)/NULLIF(COUNT(*),0),2) sla_compliance_pct
FROM returns WHERE is_open=0;
-- 5. Open backlog and average age at fixed snapshot
SELECT return_status,COUNT(*) open_cases,ROUND(AVG(DATEDIFF('2025-12-31',request_date)),1) avg_age_days
FROM returns WHERE is_open=1 GROUP BY return_status;
-- 6. Team workload
SELECT assigned_team,COUNT(*) total_cases,SUM(is_open) open_cases,
 SUM(CASE WHEN is_open=0 AND sla_met=1 THEN 1 ELSE 0 END) closed_within_sla,
 SUM(CASE WHEN is_open=0 THEN 1 ELSE 0 END) closed_cases
FROM returns GROUP BY assigned_team;
-- 7. Processing duration by reason
SELECT return_reason,ROUND(AVG(processing_days),2) avg_processing_days,COUNT(processing_days) completed_cases
FROM returns WHERE processing_days IS NOT NULL GROUP BY return_reason ORDER BY avg_processing_days DESC;
-- 8. Monthly return trend
SELECT DATE_FORMAT(o.order_date,'%Y-%m') order_month,COUNT(DISTINCT o.order_id) eligible_orders,
 COUNT(DISTINCT r.return_id) return_cases,
 ROUND(100*COUNT(DISTINCT r.return_id)/NULLIF(COUNT(DISTINCT o.order_id),0),2) return_rate_pct
FROM orders o LEFT JOIN returns r ON r.order_id=o.order_id
WHERE o.order_status IN ('Delivered','Returned') GROUP BY DATE_FORMAT(o.order_date,'%Y-%m') ORDER BY order_month;
-- 9. Orphan return keys
SELECT r.return_id,r.order_id FROM returns r LEFT JOIN orders o ON o.order_id=r.order_id WHERE o.order_id IS NULL;
-- 10. Returned order vs return record reconciliation
SELECT (SELECT COUNT(*) FROM orders WHERE order_status='Returned') returned_orders,
 (SELECT COUNT(*) FROM returns) return_records;
-- 11. Open cases beyond SLA
SELECT return_id,order_id,return_status,assigned_team,DATEDIFF('2025-12-31',request_date) case_age_days
FROM returns WHERE is_open=1 AND DATEDIFF('2025-12-31',request_date)>sla_days ORDER BY case_age_days DESC;
-- 12. Refund exposure by region
SELECT c.region,COUNT(r.return_id) cases,ROUND(SUM(r.refund_amount),2) refund_exposure
FROM returns r JOIN orders o ON o.order_id=r.order_id JOIN customers c ON c.customer_id=o.customer_id
GROUP BY c.region ORDER BY refund_exposure DESC;
