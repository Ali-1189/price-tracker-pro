def build_price_alert(product_name, price, url, old_price=None):
    if old_price:
        diff = price - old_price
        trend = "📉 انخفاض" if diff < 0 else "📈 ارتفاع"
        # رسالة احترافية للمستخدم العادي
        msg = (
            f"🔔 *تحديث في الأسعار!*\n\n"
            f"📦 *المنتج:* {product_name}\n"
            f"💰 *السعر الجديد:* {price:,.2f} EGP\n"
            f"⚖️ *الحالة:* {trend} بمقدار ({abs(diff):,.2f})\n\n"
            f"🔗 [اضغط هنا للمعاينة]({url})"
        )
    else:
        msg = (
            f"✅ *تمت الإضافة بنجاح!*\n\n"
            f"📦 جارٍ مراقبة: {product_name}\n"
            f"💰 السعر الحالي: {price:,.2f} EGP\n\n"
            f"🚀 سأقوم بتنبيهك فور تغير السعر."
        )
    return msg