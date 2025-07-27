import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config("Het Boerderijwinkeltje", layout="centered")

PRICES = {
    "Yoghurt naturel 1L": 2.10,
    "Yoghurt naturel 500ml": 1.40,
    "Yoghurt fruit 1L": 2.50,
    "Yoghurt fruit 500ml": 1.60,
    "Karnemelk 1L": 2.40,
    "Karnemelk 500ml": 1.50,
    "Melk 1L": 1.95,
    "Melk 500ml": 1.30,
    "Chocolademelk 1L": 2.45,
    "Chocolademelk 500ml": 1.80,
    "Hangop naturel 500ml": 2.50,
    "Hangop fruit 500ml": 3.00,
    "Vla vanille 1L": 2.80,
    "Vla karamel 1L": 2.90,
    "Vla bitterkoekjes 1L": 3.10,
    "Vla hopjes 1L": 3.00,
    "Vla banaan 1L": 2.90,
    "Vla chocolade 1L": 3.00,
    "Roomboter 250g": 3.50,
}

if 'log' not in st.session_state:
    st.session_state.log = []

st.title("Het Boerderijwinkeltje")
st.subheader("Nieuwe batch toevoegen")

with st.form("batch_form"):
    date = st.date_input("Datum", datetime.today())
    product = st.selectbox("Product", list(PRICES.keys()))
    qty = st.number_input("Hoeveelheid", min_value=0.0, format="%.2f")
    comment = st.text_input("Opmerkingen")
    if st.form_submit_button("Opslaan"):
        unit_price = PRICES[product]
        if "Roomboter" in product:
            total_value = qty * unit_price
            qty_display = f"{int(qty)}×250 g"
        else:
            total_value = qty * unit_price
            qty_display = f"{qty:.2f} L"
        batch_id = f"{date.strftime('%Y%m%d')}-{sum(1 for e in st.session_state.log if e['date']==date)+1:02d}"
        st.session_state.log.append({
            "ID": batch_id,
            "Datum": date.strftime("%Y-%m-%d"),
            "Product": product,
            "Hoeveelheid": qty_display,
            "Waarde (€)": f"€{total_value:.2f}",
            "Opmerkingen": comment
        })
        st.success(f"Batch {batch_id} opgeslagen!")

st.subheader("Logboek")
df = pd.DataFrame(st.session_state.log)
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.write("Nog geen batches ingevoerd.")
