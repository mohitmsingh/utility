def calculate_totals(items, gst_rate):
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    gst = subtotal * gst_rate / 100
    total = subtotal + gst
    return subtotal, gst, total