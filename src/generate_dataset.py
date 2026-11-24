import csv, random
from datetime import date, timedelta
from pathlib import Path

random.seed(73)
OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)

regions = [("North","Delhi"),("North","Jaipur"),("South","Bengaluru"),("South","Chennai"),
           ("West","Mumbai"),("West","Pune"),("East","Kolkata"),("Central","Bhopal")]
categories = {
    "Electronics":["Smartphone","Laptop","Headphones","Monitor","Smartwatch"],
    "Fashion":["Shoes","T-shirt","Jacket","Jeans","Handbag"],
    "Home & Kitchen":["Mixer Grinder","Cookware Set","Bedsheet","Storage Rack","Desk Lamp"],
    "Books & Stationery":["Notebook Set","Office Chair","Printer Paper","Pen Pack","Planner"]
}
products = []
for category, names in categories.items():
    for name in names:
        products.append({"product_id":"PR%03d" % (len(products)+1),
                         "product_name":name,"category":category})

customers = []
for i in range(1, 801):
    region, city = random.choice(regions)
    customers.append({"customer_id":"CU%04d" % i,
                      "customer_segment":random.choice(["Consumer","Corporate","Small Business"]),
                      "region":region,"city":city})

statuses = ["Requested","Pickup Scheduled","In Transit","Received","Inspection","Refund Processing","Closed","Rejected"]
reasons = ["Damaged Product","Wrong Item Delivered","Product Not as Described","Late Delivery","Size/Fit Issue","Changed Mind","Missing Parts"]
teams = ["Returns Team A","Returns Team B","Returns Team C","Escalations Team"]
start, end = date(2025,1,1), date(2025,12,31)
orders, returns = [], []

for i in range(1,10001):
    order_id = "OR%06d" % i
    order_date = start + timedelta(days=random.randint(0,(end-start).days))
    customer = random.choice(customers)
    has_return = random.random() < 0.145
    order = {
        "order_id":order_id,"order_date":order_date.isoformat(),
        "customer_id":customer["customer_id"],
        "product_id":random.choice(products)["product_id"],
        "quantity":random.randint(1,4),
        "order_value":round(random.uniform(250,45000),2),
        "order_status":"Returned" if has_return else random.choices(
            ["Delivered","Cancelled","In Transit"],[0.91,0.04,0.05])[0],
        "sales_channel":random.choice(["App","Website","Marketplace"])
    }
    orders.append(order)
    if has_return:
        request_date = order_date + timedelta(days=random.randint(1,18))
        status = random.choices(statuses,[5,7,8,10,8,12,45,5])[0]
        is_closed = status in ["Closed","Rejected"]
        processing_days = random.randint(1,12) if is_closed else ""
        returns.append({
            "return_id":"RT%06d" % (len(returns)+1),"order_id":order_id,
            "request_date":request_date.isoformat(),
            "pickup_date":(request_date+timedelta(days=random.randint(1,3))).isoformat(),
            "received_date":(request_date+timedelta(days=random.randint(3,7))).isoformat(),
            "closed_date":(request_date+timedelta(days=processing_days)).isoformat() if is_closed else "",
            "return_reason":random.choice(reasons),"return_status":status,
            "return_channel":random.choice(["App","Website","Customer Support"]),
            "assigned_team":random.choice(teams),
            "refund_amount":round(order["order_value"]*random.uniform(0.7,1.0),2),
            "sla_days":5,"processing_days":processing_days,
            "sla_met":1 if is_closed and processing_days <= 5 else 0,
            "is_open":0 if is_closed else 1
        })

def write_csv(filename, rows):
    with (OUT / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

write_csv("orders.csv",orders)
write_csv("returns.csv",returns)
write_csv("customers.csv",customers)
write_csv("products.csv",products)
print("Generated %d orders, %d returns, %d customers and %d products." %
      (len(orders),len(returns),len(customers),len(products)))
