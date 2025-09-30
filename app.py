
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from calculations.cost_model import load_base_rates, estimate_cost

def main():
    st.set_page_config(page_title="تخمین قیمت پروژه کامپوزیت", layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background-color: #f0f8ff; direction: rtl; font-family: IRANSans; }
        .sidebar .sidebar-content { background-color: #e6f2ff; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    try:
        st.image("assets/logo.png", width=200)
    except:
        pass

    st.title("🧮 تخمین قیمت پروژه‌های پوشش کامپوزیتی")

    project_type = st.selectbox("نوع پروژه", ["کف", "مخزن", "خط لوله"])
    area = st.number_input("مساحت پروژه (متر مربع)", min_value=1.0, step=1.0)
    resin_price = st.number_input("قیمت روز رزین (تومان / کیلوگرم)", min_value=0.0, step=100.0)
    difficulty_factor = st.slider("ضریب سختی محیط اجرا", 1.0, 2.0, 1.0, 0.05)

    if st.button("محاسبه"):
        base_rates = load_base_rates()
        params = {
            "project_type": project_type,
            "area": area,
            "resin_price": resin_price,
            "difficulty_factor": difficulty_factor
        }
        res = estimate_cost(params, base_rates)

        st.subheader("نتیجه برآورد")
        st.write(f"✅ قیمت هر متر مربع اجرا: **{res['price_per_m2']:.0f} تومان**")
        st.write(f"✅ قیمت کل پروژه: **{res['total_price']:.0f} تومان**")

        st.subheader("جزئیات هزینه‌ها")
        df = pd.DataFrame({
            "مؤلفه": ["متریال", "اجرا", "تجهیزات", "جمع بدون سود"],
            "هزینه (تومان)": [
                res["material_cost"],
                res["labor_cost"],
                res["equip_cost"],
                res["total_before_markup"]
            ]
        })
        st.table(df)

        st.subheader("نمودار سهم هزینه‌ها")
        labels = ["متریال", "اجرا", "تجهیزات"]
        sizes = [res["material_cost"], res["labor_cost"], res["equip_cost"]]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
