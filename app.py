import io
import pandas as pd
import streamlit as st
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

st.set_page_config(page_title="सहकारी संस्था ऑडिट प्रणाली", layout="wide")

st.title("📑 सहकारी संस्था वैधानिक लेखापरीक्षण अहवाल जनरेटर")
st.caption("ट्रायल बॅलन्स एक्सेल अपलोड करा आणि ताळेबंद, नफा-तोटा, फॉर्म 'न' व फॉर्म 'ओ' एकाच PDF मध्ये मिळवा.")

# १. संस्थेची प्राथमिक माहिती
st.sidebar.header("🏢 १. संस्थेचा तपशील")
sanstha_name = st.sidebar.text_input("संस्थेचे नाव", "श्री गणेश सहकारी पतसंस्था मर्यादित")
address = st.sidebar.text_input("पत्ता", "मुख्य रस्ता, लातूर")
reg_no = st.sidebar.text_input("नोंदणी क्रमांक", "LTR/BNK/123/2015")
fin_year = st.sidebar.text_input("आर्थिक वर्ष", "२०२५-२०२६")

# २. फॉर्म 'न' तपशील
st.sidebar.markdown("---")
st.sidebar.header("🏅 २. फॉर्म 'न' (ऑडिट वर्गीकरण)")
audit_class = st.sidebar.selectbox("ऑडिट वर्ग (Audit Class)", ["'अ' (A)", "'ब' (B)", "'क' (C)", "'ड' (D)"])
auditor_name = st.sidebar.text_input("लेखापरीक्षकाचे नाव", "सनदी लेखापाल / पॅनेल ऑडिटर")
audit_date = st.sidebar.date_input("ऑडिट पूर्ण दिनांक", value=datetime.today())

with st.sidebar.expander("गुणदान तपशील (कमाल १०० गुण)"):
    m_financial = st.slider("भांडवली व आर्थिक स्थिती (कमाल २५)", 0, 25, 22)
    m_loan = st.slider("व्यवसाय व वसुली (कमाल २५)", 0, 25, 20)
    m_mgmt = st.slider("व्यवस्थापन व वैधानिक बाबी (कमाल २५)", 0, 25, 21)
    m_accounts = st.slider("हिशोब व अंतर्गत तपासणी (कमाल २५)", 0, 25, 22)

total_marks = m_financial + m_loan + m_mgmt + m_accounts
st.sidebar.info(f"एकूण भरलेले गुण: {total_marks} / १००")

# मुख्य स्क्रीन: एक्सेल अपलोड
st.subheader("📂 कच्चा ताळेबंद (Trial Balance) एक्सेल फाइल")
uploaded_file = st.file_uploader("एक्सेल (.xlsx) फाइल निवडा (कॉलम्स: 'खात्याचे नाव', 'Type', 'Debit', 'Credit')", type=["xlsx", "xls"])

# नमुना डेटा डाऊनलोड करण्यासाठी बटण (मदतीसाठी)
sample_df = pd.DataFrame([
    {"खात्याचे नाव": "शेअर भांडवल", "Type": "Liability", "Debit": 0, "Credit": 500000},
    {"खात्याचे नाव": "राखीव निधी", "Type": "Liability", "Debit": 0, "Credit": 120000},
    {"खात्याचे नाव": "बँक चालू खाते शिल्लक", "Type": "Asset", "Debit": 350000, "Credit": 0},
    {"खात्याचे नाव": "रोख शिल्लक", "Type": "Asset", "Debit": 25000, "Credit": 0},
    {"खात्याचे नाव": "सभासदांना कर्ज येणे", "Type": "Asset", "Debit": 245000, "Credit": 0},
    {"खात्याचे नाव": "कर्जावरील व्याज उत्पन्न", "Type": "Income", "Debit": 0, "Credit": 45000},
    {"खात्याचे नाव": "कर्मचारी पगार खर्च", "Type": "Expense", "Debit": 30000, "Credit": 0},
    {"खात्याचे नाव": "स्टेशनरी व छपाई खर्च", "Type": "Expense", "Debit": 10000, "Credit": 0},
])

st.download_button(
    label="📥 नमुना एक्सेल टेम्पलेट डाऊनलोड करा",
    data=io.BytesIO(sample_df.to_csv(index=False).encode('utf-8')),
    file_name="sample_trial_balance.csv",
    mime="text/csv"
)

st.markdown("---")

# ३. फॉर्म 'ओ' (दोष दुरुस्ती) टेबल
st.subheader("📝 ३. फॉर्म 'ओ' (दोष दुरुस्ती अहवाल तपशील)")
default_rectifications = [
    {
        "ऑडिट परिच्छेद क्र.": "१ (अ)",
        "लेखापरीक्षणातील आक्षेप / दोष": "काही खर्चाच्या व्हाउचर्सवर व्यवस्थापकांची स्वाक्षरी प्रलंबित होती.",
        "संस्थेने केलेली दुरुस्ती / खुलासा": "सदर व्हाउचर्सवर आवश्यक त्या स्वाक्षऱ्या घेऊन दुरुस्ती करण्यात आली.",
        "दुरुस्तीचा दिनांक": "15/05/2026",
        "पुनरावलोकन शेरा": "दोष दुरुस्त झाला."
    },
    {
        "ऑडिट परिच्छेद क्र.": "२ (ब)",
        "लेखापरीक्षणातील आक्षेप / दोष": "३१ मार्च अखेरचे बँक मेळ जुळवणी पत्रक (BRS) उपलब्ध नव्हते.",
        "संस्थेने केलेली दुरुस्ती / खुलासा": "सर्व बँकांचे मार्च अखेरचे BRS तयार करून हिशोबाशी ताळमेळ घातला आहे.",
        "दुरुस्तीचा दिनांक": "20/05/2026",
        "पुनरावलोकन शेरा": "दुरुस्ती मान्य."
    }
]

col_m1, col_m2 = st.columns(2)
meeting_date = col_m1.text_input("संचालक मंडळ सभा दिनांक", "10/06/2026")
resolution_no = col_m2.text_input("मंजूर ठराव क्रमांक", "ठराव क्र. ५")

rectification_df = st.data_editor(
    pd.DataFrame(default_rectifications),
    num_rows="dynamic",
    use_container_width=True
)

st.markdown("---")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        required_cols = ['खात्याचे नाव', 'Type', 'Debit', 'Credit']
        if not all(col in df.columns for col in required_cols):
            st.error("एक्सेल फाइलमध्ये 'खात्याचे नाव', 'Type', 'Debit', 'Credit' हे चारही कॉलम्स असणे अनिवार्य आहे!")
        else:
            df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce').fillna(0.0)
            df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0.0)

            # नफा-तोटा आकडेमोड
            incomes = df[df['Type'] == 'Income'].copy()
            incomes['Final'] = incomes['Credit'] - incomes['Debit']
            total_income = incomes['Final'].sum()

            expenses = df[df['Type'] == 'Expense'].copy()
            expenses['Final'] = expenses['Debit'] - expenses['Credit']
            total_expense = expenses['Final'].sum()

            net_profit = total_income - total_expense

            # ताळेबंद आकडेमोड
            liabilities = df[df['Type'] == 'Liability'].copy()
            liabilities['Final'] = liabilities['Credit'] - liabilities['Debit']

            assets = df[df['Type'] == 'Asset'].copy()
            assets['Final'] = assets['Debit'] - assets['Credit']

            liab_list = liabilities[['खात्याचे नाव', 'Final']].to_dict(orient='records')
            if net_profit >= 0:
                liab_list.append({'खात्याचे नाव': 'चालू वर्षाचा निव्वळ नफा (Net Profit)', 'Final': net_profit})
            else:
                liab_list.append({'खात्याचे नाव': 'चालू वर्षाचा निव्वळ तोटा (Net Loss)', 'Final': net_profit})

            total_liability = liabilities['Final'].sum() + net_profit
            total_assets = assets['Final'].sum()

            # सारांश डॅशबोर्ड
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("एकूण उत्पन्न (Income)", f"₹ {total_income:,.2f}")
            kpi2.metric("एकूण खर्च (Expense)", f"₹ {total_expense:,.2f}")
            kpi3.metric("निव्वळ नफा / तोटा", f"₹ {net_profit:,.2f}")
            
            diff = abs(total_liability - total_assets)
            if diff < 0.01:
                kpi4.success(f"ताळेबंद Tally! (₹ {total_assets:,.2f}) ✅")
            else:
                kpi4.error(f"ताळेबंद फरक: ₹ {diff:,.2f} ⚠️")

            # PDF जनरेशन बटण
            if st.button("🚀 संपूर्ण ऑडिट अहवाल PDF जनरेट करा", type="primary"):
                with st.spinner("PDF तयार होत आहे, कृपया थांबा..."):
                    env = Environment(loader=FileSystemLoader("templates"))
                    template = env.get_template("final_accounts.html")

                    rendered_html = template.render(
                        sanstha_name=sanstha_name,
                        address=address,
                        reg_no=reg_no,
                        fin_year=fin_year,
                        # नफा-तोटा
                        incomes=incomes.to_dict(orient='records'),
                        expenses=expenses.to_dict(orient='records'),
                        total_income=total_income,
                        total_expense=total_expense,
                        net_profit=net_profit,
                        # ताळेबंद
                        liabilities=liab_list,
                        assets=assets.to_dict(orient='records'),
                        total_liability=total_liability,
                        total_assets=total_assets,
                        # फॉर्म 'न'
                        audit_class=audit_class,
                        m_financial=m_financial,
                        m_loan=m_loan,
                        m_mgmt=m_mgmt,
                        m_accounts=m_accounts,
                        total_marks=total_marks,
                        auditor_name=auditor_name,
                        audit_date=audit_date.strftime('%d/%m/%Y'),
                        # फॉर्म 'ओ'
                        rectifications=rectification_df.to_dict(orient='records'),
                        meeting_date=meeting_date,
                        resolution_no=resolution_no
                    )

                    pdf_bytes = HTML(string=rendered_html).write_pdf()

                    st.success("संपूर्ण अहवाल यशस्वीरित्या तयार झाला!")
                    st.download_button(
                        label="📥 डाऊनलोड संपूर्ण ऑडिट अहवाल (PDF)",
                        data=pdf_bytes,
                        file_name=f"Full_Audit_Report_{fin_year}.pdf",
                        mime="application/pdf"
                    )

    except Exception as e:
        st.error(f"डेटा प्रक्रिया करताना त्रुटी आली: {str(e)}")
else:
    st.info("कृपया ऑडिट रिपोर्ट तयार करण्यासाठी एक्सेल फाइल अपलोड करा.")
