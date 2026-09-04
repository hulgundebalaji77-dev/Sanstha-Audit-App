import io
import pandas as pd
import streamlit as st
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

st.set_page_config(page_title="संस्था संपूर्ण ऑडिट रिपोर्ट", layout="wide")
st.title("📑 संस्था ताळेबंद व नफा-तोटा पत्रक जनरेटर")

# संस्थेचा तपशील
st.sidebar.header("संस्थेची माहिती")
sanstha_name = st.sidebar.text_input("संस्थेचे नाव", "श्री गणेश सहकारी पतसंस्था मर्या.")
address = st.sidebar.text_input("पत्ता", "लातूर")
fin_year = st.sidebar.text_input("आर्थिक वर्ष", "२०२५-२०२६")

uploaded_file = st.file_uploader("ट्रायल बॅलन्स एक्सेल अपलोड करा", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce').fillna(0.0)
    df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0.0)
    
    # निव्वळ रक्कम काढणे (Net Amount)
    # Income/Liability: Credit - Debit | Asset/Expense: Debit - Credit
    df['Amount'] = 0.0
    
    # Income & Expenditure वेगळे करणे
    incomes = df[df['Type'] == 'Income'].copy()
    incomes['Final'] = incomes['Credit'] - incomes['Debit']
    total_income = incomes['Final'].sum()
    
    expenses = df[df['Type'] == 'Expense'].copy()
    expenses['Final'] = expenses['Debit'] - expenses['Credit']
    total_expense = expenses['Final'].sum()
    
    net_profit = total_income - total_expense  # धन असल्यास नफा, ऋण असल्यास तोटा

    # Balance Sheet बाजू वेगळ्या करणे
    liabilities = df[df['Type'] == 'Liability'].copy()
    liabilities['Final'] = liabilities['Credit'] - liabilities['Debit']
    
    assets = df[df['Type'] == 'Asset'].copy()
    assets['Final'] = assets['Debit'] - assets['Credit']
    
    # चालू वर्षाचा नफा/तोटा देयता (Liability) बाजूस जोडणे
    liab_list = liabilities[['खात्याचे नाव', 'Final']].to_dict(orient='records')
    if net_profit >= 0:
        liab_list.append({'खात्याचे नाव': 'चालू वर्षाचा निव्वळ नफा (Net Profit)', 'Final': net_profit})
    else:
        liab_list.append({'खात्याचे नाव': 'चालू वर्षाचा निव्वळ तोटा (Net Loss)', 'Final': net_profit})
        
    total_liability = liabilities['Final'].sum() + net_profit
    total_assets = assets['Final'].sum()

    # डॅशबोर्डवर दाखवणे
    c1, c2, c3 = st.columns(3)
    c1.metric("एकूण उत्पन्न (Income)", f"₹ {total_income:,.2f}")
    c2.metric("एकूण खर्च (Expenditure)", f"₹ {total_expense:,.2f}")
    c3.metric("निव्वळ नफा / (तोटा)", f"₹ {net_profit:,.2f}")

    diff = abs(total_liability - total_assets)
    if diff < 0.01:
        st.success(f"ताळेबंद पूर्णपणे जुळला आहे! एकूण: ₹ {total_assets:,.2f} ✅")
    else:
        st.error(f"ताळेबंदामध्ये फरक आहे: ₹ {diff:,.2f} ⚠️")

    if st.button("📄 ताळेबंद व नफा-तोटा PDF तयार करा"):
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("final_accounts.html")
        
        rendered_html = template.render(
            sanstha_name=sanstha_name,
            address=address,
            fin_year=fin_year,
            incomes=incomes.to_dict(orient='records'),
            expenses=expenses.to_dict(orient='records'),
            total_income=total_income,
            total_expense=total_expense,
            net_profit=net_profit,
            liabilities=liab_list,
            assets=assets.to_dict(orient='records'),
            total_liability=total_liability,
            total_assets=total_assets
        )
        
        pdf_bytes = HTML(string=rendered_html).write_pdf()
        st.download_button("📥 डाऊनलोड फायनल ऑडिट रिपोर्ट (PDF)", pdf_bytes, file_name=f"Final_Audit_{fin_year}.pdf")
