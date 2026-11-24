# Power Query M Guide

Import each CSV using Get Data → Text/CSV and assign explicit types.

## Orders
```powerquery
let
 Source = Csv.Document(File.Contents("C:\PATH\data\orders.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Types = Table.TransformColumnTypes(Headers,{
  {"order_id",type text},{"order_date",type date},{"customer_id",type text},{"product_id",type text},
  {"quantity",Int64.Type},{"order_value",Currency.Type},{"order_status",type text},{"sales_channel",type text}}),
 Clean = Table.TransformColumns(Types,{{"order_status",Text.Trim,type text},{"sales_channel",Text.Trim,type text}}),
 Unique = Table.Distinct(Clean,{"order_id"})
in Unique
```

## Returns
```powerquery
let
 Source = Csv.Document(File.Contents("C:\PATH\data\returns.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Types = Table.TransformColumnTypes(Headers,{
  {"return_id",type text},{"order_id",type text},{"request_date",type date},{"pickup_date",type date},
  {"received_date",type date},{"closed_date",type date},{"return_reason",type text},{"return_status",type text},
  {"return_channel",type text},{"assigned_team",type text},{"refund_amount",Currency.Type},
  {"sla_days",Int64.Type},{"processing_days",Int64.Type},{"sla_met",Int64.Type},{"is_open",Int64.Type}}),
 Clean = Table.TransformColumns(Types,{{"return_reason",Text.Trim,type text},{"return_status",Text.Trim,type text},{"assigned_team",Text.Trim,type text}}),
 Unique = Table.Distinct(Clean,{"return_id"})
in Unique
```

For customers/products, set IDs and labels to Text, remove duplicate keys after checking them, and validate foreign keys. Preserve blank close dates and processing days for open cases; do not discard open cases.
