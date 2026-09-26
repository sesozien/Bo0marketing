import streamlit as st
import pandas as pd
from PIL import Image

# ---------------------------------------------------------
# 1. إعدادات الصفحة والستايل المريح للعين
# ---------------------------------------------------------
st.set_page_config(
    page_title="مدير المنتجات وصانع منشورات فيسبوك",
    page_icon="📦",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .product-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    .post-box {
        background-color: #eef2f5;
        border-right: 5px solid #1877f2;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        white-space: pre-wrap;
    }
    div[data-baseweb="input"] input:placeholder-shown {
        background-color: #fff9db !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة الحالة (Session State)
# ---------------------------------------------------------
if "categories" not in st.session_state:
    st.session_state.categories = ["توك واكسسوارات", "خردوات", "استانليس", "بلاستيكات", "شغل مواسم"]

if "catalog" not in st.session_state:
    st.session_state.catalog = []

# قاعدة بيانات الهاشتاجات حسب الصنف + التريند
CATEGORY_HASHTAGS = {
    "توك واكسسوارات": ["#توك_شعر", "#اكسسوارات_بنات", "#توك_اطفال", "#موضة_بنات", "#اكسسوارات_جملة", "#هدايا_بنات"],
    "خردوات": ["#خردوات", "#أدوات_منزلية", "#مستلزمات_بيت", "#تجهيز_عرائس", "#خردوات_جملة", "#أدوات_المطبخ"],
    "استانليس": ["#استانليس", "#استانلس_ستيل", "#مطبخ_حديث", "#أدوات_مطبخ", "#تجهيزات_مطابخ", "#جودة_عالية"],
    "بلاستيكات": ["#بلاستيكات", "#أدوات_بلاستيكية", "#منظمات_منزلية", "#مستلزمات_منزل", "#بلاستيكات_جملة"],
    "شغل مواسم": ["#شغل_مواسم", "#عروض_المواسم", "#تخفيضات_حصري", "#تجهيزات_العيد", "#منتجات_موسمية", "#عروض_خاصة"]
}

TRENDING_HASHTAGS = ["#مصر", "#تجارة_جملة", "#شحن_لجميع_المحافظات", "#توصيل_سريع", "#أونلاين_شوبينج", "#تسوق_الان", "#عروض_اليوم"]

# ---------------------------------------------------------
# 3. الشريط الجانبي: إدارة التصنيفات ومعلومات التواصل
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ إدارة التصنيفات")
    new_cat = st.text_input("إضافة تصنيف جديد:")
    if st.button("➕ إضافة التصنيف"):
        if new_cat and new_cat not in st.session_state.categories:
            st.session_state.categories.append(new_cat)
            st.success(f"تمت إضافة: {new_cat}")
        elif new_cat in st.session_state.categories:
            st.warning("التصنيف موجود بالفعل!")

    st.divider()
    st.header("📞 بيانات التواصل الثابتة")
    st.caption("أدخل بياناتك لتظهر تلقائياً في بوستات الفيسبوك:")
    contact_phone = st.text_input("رقم الهاتف للاتصال:", "01000000000")
    whatsapp_num = st.text_input("رقم الواتساب (للرابط المباشر):", "201000000000")
    fb_page_link = st.text_input("رابط صفحة الفيسبوك:", "https://facebook.com/yourpage")
    store_address = st.text_input("العنوان / الشحن:", "القاهرة - شحن لجميع المحافظات 🚚")

# ---------------------------------------------------------
# 4. الواجهة الرئيسية: إدخال المنتجات
# ---------------------------------------------------------
st.title("📦 أداة إدارة المنتجات وصانع بوستات الفيسبوك")
st.write("أدخل بيانات المنتج لبناء الكتالوج وتوليد منشورات جاهزة للنشر فوراً.")

st.divider()

col_img, col_inputs = st.columns([1, 2])

with col_img:
    st.subheader("🖼️ صورة المنتج")
    uploaded_image = st.file_uploader("ارفع صورة المنتج", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="معاينة الصورة", use_column_width=True)

with col_inputs:
    st.subheader("📝 بيانات المنتج")
    
    col1, col2 = st.columns(2)
    with col1:
        prod_name = st.text_input("اسم المنتج *", placeholder="أدخل اسم المنتج")
        prod_code = st.text_input("كود المنتج", placeholder="اتركه فارغاً إن لم يوجد")
        category = st.selectbox("تصنيف المنتج", options=st.session_state.categories)
    
    with col2:
        dozen_price = st.number_input("السعر للدستة (12 قطعة)", min_value=0.0, value=0.0, step=0.5)
        
        # حساب سعر القطعة تلقائياً
        unit_price = dozen_price / 12.0 if dozen_price > 0 else 0.0
        st.number_input("السعر للقطعة (محسوب تلقائياً)", value=round(unit_price, 2), disabled=True)
        
        carton_qty = st.number_input("عدد الكرتونة", min_value=0, value=0, step=1)
        carton_price = st.number_input("سعر الكرتونة", min_value=0.0, value=0.0, step=1.0)

# تنبيه الخانات الفارغة
empty_fields = []
if not prod_name: empty_fields.append("اسم المنتج")
if not prod_code: empty_fields.append("كود المنتج")
if dozen_price == 0: empty_fields.append("سعر الدستة")
if carton_qty == 0: empty_fields.append("عدد الكرتونة")
if carton_price == 0: empty_fields.append("سعر الكرتونة")

if empty_fields:
    st.info(f"💡 الخانات المتبقية فارغة وستظهر ملونة باللون الأصفر: {', '.join(empty_fields)}")

# زر الإضافة للكتالوج
if st.button("➕ إضافة المنتج للكتالوج", type="primary", use_container_width=True):
    if not prod_name:
        st.error("⚠️ يرجى إدخال اسم المنتج على الأقل!")
    else:
        product_data = {
            "الصورة": uploaded_image,
            "الاسم": prod_name,
            "الكود": prod_code if prod_code else "غير محدد",
            "التصنيف": category,
            "سعر الدستة": dozen_price if dozen_price > 0 else "غير محدد",
            "سعر القطعة": round(unit_price, 2) if unit_price > 0 else "غير محدد",
            "عدد الكرتونة": carton_qty if carton_qty > 0 else "غير محدد",
            "سعر الكرتونة": carton_price if carton_price > 0 else "غير محدد",
        }
        st.session_state.catalog.append(product_data)
        st.success(f"تمت إضافة ({prod_name}) إلى الكتالوج بنجاح!")

# ---------------------------------------------------------
# 5. صانع ومولد بوستات فيسبوك الذكي 🔥
# ---------------------------------------------------------
st.divider()
st.header("📲 مولّد بوستات الفيسبوك والهاشتاجات")

if not prod_name:
    st.warning("👈 يرجى إدخال اسم المنتج في النموذج بالأعلى أولاً لتوليد البوست!")
else:
    col_post_settings, col_post_preview = st.columns([1, 1])

    with col_post_settings:
        st.subheader("⚙️ إعدادات البوست")
        
        post_style = st.selectbox(
            "طبيعة/أسلوب المنشور:",
            ["💥 عرض خاص وتخفيضات", "🏬 تجارة جملة للمحلات والموزعين", "🌟 عرض قطاعي راقي وشيك"]
        )
        
        price_display_option = st.selectbox(
            "إظهار أي أسعار في البوست؟",
            ["سعر القطعة وسعر الدستة", "سعر الدستة فقط", "سعر القطعة فقط", "سعر الكرتونة والدستة", "بدون أسعار (السعر في الخاص/الواتساب)"]
        )

        custom_intro = st.text_area(
            "صيغة/مقدمة البوست (اختياري - اتركه فارغاً لإنشاء مقدمة تلقائية):",
            placeholder="مثال: وصل حديثاً أقوى الموديلات للبيت والمطبخ! خامات ممتازة وأسعار زمان..."
        )

        st.subheader("🏷️ مولّد الهاشتاجات")
        
        # تجميع الهاشتاجات التلقائية
        cat_tags = CATEGORY_HASHTAGS.get(category, ["#منتجات_مميزة"])
        all_auto_tags = cat_tags + TRENDING_HASHTAGS
        
        selected_hashtags = st.multiselect(
            f"الهاشتاجات المقترحة لصنف ({category}) والتريند:",
            options=all_auto_tags,
            default=all_auto_tags[:6]
        )
        
        custom_hashtags = st.text_input("أضف هاشتاجات إضافية (افصل بينها بمسافات):", "#اسم_محلكم #جديد")

    # بناء نص البوست تلقائياً
    with col_post_preview:
        st.subheader("📝 معاينة البوست الجاهز للنشر")

        # 1. المقدمة
        if custom_intro.strip():
            post_text = f"{custom_intro.strip()}\n\n"
        else:
            if "عرض خاص" in post_style:
                post_text = f"🔥 **عرض خاص لفترة محدودة!** 🔥\n✨ أحدث موديلات قسم (**{category}**) وصل الآن!\n\n"
            elif "جملة" in post_style:
                post_text = f"📢 **لأصحاب المحلات وتجار الجملة!** 📢\nتشكيلة جديدة ممتازة وصلت من صنف (**{category}**).\n\n"
            else:
                post_text = f"🌟 **شياكة وجودة مفيش منها!** 🌟\nبنقدملك أفضل خامة وأحسن سعر فـ (**{category}**).\n\n"

        # 2. تفاصيل المنتج
        post_text += f"📦 **اسم المنتج:** {prod_name}\n"
        if prod_code:
            post_text += f"🔢 **كود المنتج:** {prod_code}\n"
        
        # 3. الأسعار حسب اختيار المستخدم
        if price_display_option == "سعر القطعة وسعر الدستة":
            if dozen_price > 0: post_text += f"💰 **سعر الدستة (12 قطعة):** {dozen_price} ج.م\n"
            if unit_price > 0: post_text += f"💵 **سعر القطعة:** {round(unit_price, 2)} ج.م\n"
        elif price_display_option == "سعر الدستة فقط" and dozen_price > 0:
            post_text += f"💰 **سعر الدستة (12 قطعة):** {dozen_price} ج.م\n"
        elif price_display_option == "سعر القطعة فقط" and unit_price > 0:
            post_text += f"💵 **سعر القطعة:** {round(unit_price, 2)} ج.م\n"
        elif price_display_option == "سعر الكرتونة والدستة":
            if dozen_price > 0: post_text += f"💰 **سعر الدستة:** {dozen_price} ج.م\n"
            if carton_price > 0: post_text += f"📦 **سعر الكرتونة:** {carton_price} ج.م ({carton_qty} قطعة)\n"
        elif price_display_option == "بدون أسعار (السعر في الخاص/الواتساب)":
            post_text += "💬 **السعر:** تواصل معنا على الواتساب لمعرفة أحسن سعر للجملة!\n"

        if carton_qty > 0 and price_display_option != "سعر الكرتونة والدستة":
            post_text += f"📦 **عدد القطع بالكرتونة:** {carton_qty} قطعة\n"

        # 4. روابط التواصل والمعلومات
        post_text += "\n-----------------------------------\n"
        post_text += "📲 **للطلب والاستفسار تواصل معنا فوراً:**\n"
        if whatsapp_num:
            post_text += f"💬 **واتساب مباشر:** https://wa.me/{whatsapp_num.replace('+', '').strip()}\n"
        if contact_phone:
            post_text += f"📞 **موبايل:** {contact_phone}\n"
        if fb_page_link:
            post_text += f"🌐 **صفحتنا على فيسبوك:** {fb_page_link}\n"
        if store_address:
            post_text += f"📍 **العنوان والشحن:** {store_address}\n"

        # 5. دمج الهاشتاجات
        post_text += "\n"
        final_tags = " ".join(selected_hashtags) + " " + custom_hashtags.strip()
        post_text += f"{final_tags}\n"

        # عرض البوست في صندوق مخصص
        st.markdown(f'<div class="post-box">{post_text}</div>', unsafe_allow_html=True)
        st.caption("✂️ يمكنك تحديد النص بأكمله بالأعلى ونسخه فوراً إلى صفحة فيسبوك.")

# ---------------------------------------------------------
# 6. عرض الكتالوج الحالي وتصديره
# ---------------------------------------------------------
st.divider()
st.header("📖 الكتالوج الحالي")

if not st.session_state.catalog:
    st.write("لا توجد منتجات في الكتالوج حتى الآن.")
else:
    selected_filter = st.selectbox("فلترة الكتالوج حسب التصنيف:", ["الكل"] + st.session_state.categories)
    
    filtered_catalog = st.session_state.catalog
    if selected_filter != "الكل":
        filtered_catalog = [p for p in st.session_state.catalog if p["التصنيف"] == selected_filter]

    for idx, item in enumerate(filtered_catalog):
        with st.container():
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 3])
            
            with c1:
                if item["الصورة"]:
                    st.image(item["الصورة"], width=150)
                else:
                    st.warning("لا توجد صورة")
            
            with c2:
                st.subheader(f"{item['الاسم']} ({item['التصنيف']})")
                st.write(f"**الكود:** {item['الكود']}")
                
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.write(f"**سعر الدستة:** {item['سعر الدستة']}")
                    st.write(f"**سعر القطعة:** {item['سعر القطعة']}")
                with p_col2:
                    st.write(f"**عدد الكرتونة:** {item['عدد الكرتونة']}")
                    st.write(f"**سعر الكرتونة:** {item['سعر الكرتونة']}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📥 تصدير البيانات")
    df_export = pd.DataFrame(st.session_state.catalog).drop(columns=["الصورة"])
    csv_data = df_export.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="📄 تحميل الكتالوج كملف Excel (CSV)",
        data=csv_data,
        file_name="catalog_products.csv",
        mime="text/csv"
    )
