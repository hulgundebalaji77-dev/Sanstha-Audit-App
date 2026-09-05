import streamlit as st
import pandas as pd
import io
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Page Configuration
st.set_page_config(
    page_title="सहकारी संस्था वैधानिक लेखापरीक्षण (ऑडिट) प्रणाली",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Session State Initialization (Default Data)
# -------------------------------------------------------------
if "society" not in st.session_state:
    st.session_state.society = {
        "name": "श्री गणेश ग्रामीण बिगरशेती सहकारी पतसंस्था मर्यादित",
        "reg_no": "RGD/BSR/1435/2012 दि. 12/05/2012",
        "address": "मु. पो. ता. निपाणी, जि. कोल्हापूर",
        "fin_year": "2023-2024 (दि. ०१/०४/२०२३ ते ३१/०३/२०२४)",
        "soc_type": "नागरी / ग्रामीण बिगरशेती सहकारी पतसंस्था",
        "members": 150,
        "auditor": "सी.ए. राजेश कुलकर्णी अँड असोसिएट्स",
        "order_no": "DDR/KOP/AUDIT/ORDER/4412 दि. 15/05/2024",
        "audit_class": "'अ' वर्ग (A Class)"
    }

if "teharij_liab" not in st.session_state:
    st.session_state.teharij_liab = pd.DataFrame([
        {"तपशील": "भाग भांडवल (Share Capital)", "रक्कम": 1520000},
        {"तपशील": "राखीव निधी (Reserve Fund)", "रक्कम": 450000},
        {"तपशील": "इतर फंड व निधी", "रक्कम": 210000},
        {"तपशील": "ठेवी (सभासद व इतर)", "रक्कम": 3850000},
        {"तपशील": "चालू वर्षाचा निव्वळ नफा", "रक्कम": 385000}
    ])

if "teharij_assets" not in st.session_state:
    st.session_state.teharij_assets = pd.DataFrame([
        {"तपशील": "सभासदांकडील कर्ज बाकी", "रक्कम": 4850000},
        {"तपशील": "गुंतवणूक (डीसीसी बँक ठेवी व शेअर्स)", "रक्कम": 1000000},
        {"तपशील": "डेडस्टॉक व फर्निचर (घसारा वजा)", "रक्कम": 285000},
        {"तपशील": "बँक शिल्लक खाती", "रक्कम": 242000},
        {"तपशील": "हातशिल्लक (कॅश)", "रक्कम": 38000}
    ])

if "loans" not in st.session_state:
    st.session_state.loans = pd.DataFrame([
        {"खाते क्र.": "101", "सभासदाचे नाव": "सुनील मारुती पाटील", "कर्ज प्रकार": "तारण कर्ज", "मंजूर दिनांक": "15/04/2023", "मंजूर रक्कम": 300000, "शिल्लक मुद्दल": 210000, "थकीत रक्कम": 0, "स्थिती": "नियमित"},
        {"खाते क्र.": "102", "सभासदाचे नाव": "तानाजी विठ्ठल शिंदे", "कर्ज प्रकार": "वैयक्तिक कर्ज", "मंजूर दिनांक": "10/06/2023", "मंजूर रक्कम": 150000, "शिल्लक मुद्दल": 95000, "थकीत रक्कम": 15000, "स्थिती": "मध्यम थकबाकी"},
        {"खाते क्र.": "103", "सभासदाचे नाव": "रमेश बापूराव देशमुख", "कर्ज प्रकार": "व्यापार कर्ज", "मंजूर दिनांक": "22/07/2023", "मंजूर रक्कम": 500000, "शिल्लक मुद्दल": 420000, "थकीत रक्कम": 0, "स्थिती": "नियमित"}
    ])

if "directors" not in st.session_state:
    st.session_state.directors = pd.DataFrame([
        {"अ.क्र.": 1, "संचालकाचे नाव": "श्री. चंद्रकांत तुकाराम माने", "पद / हुद्दा": "अध्यक्ष (Chairman)", "मुदत": "2021-2026", "संस्थेकडील कर्ज": 0, "हजेरी %": "95%", "शेरा": "पात्र व नियमित"},
        {"अ.क्र.": 2, "संचालकाचे नाव": "श्री. बाळासाहेब संभाजी पवार", "पद / हुद्दा": "उपाध्यक्ष (Vice Chairman)", "मुदत": "2021-2026", "संस्थेकडील कर्ज": 50000, "हजेरी %": "90%", "शेरा": "नियमित परतफेड"},
        {"अ.क्र.": 3, "संचालकाचे नाव": "श्री. विष्णू महादेव खोत", "पद / हुद्दा": "संचालक (Director)", "मुदत": "2021-2026", "संस्थेकडील कर्ज": 0, "हजेरी %": "85%", "शेरा": "पात्र"}
    ])

if "shares" not in st.session_state:
    st.session_state.shares = pd.DataFrame([
        {"सभासद क्र.": "M-01", "नाव": "सुनील मारुती पाटील", "सर्टिफिकेट क्र.": "C-101", "शेअर्स": 100, "दर्शनी मूल्य": 100, "एकूण रक्कम": 10000, "दिनांक": "12/05/2015"},
        {"सभासद क्र.": "M-02", "नाव": "तानाजी विठ्ठल शिंदे", "सर्टिफिकेट क्र.": "C-102", "शेअर्स": 50, "दर्शनी मूल्य": 100, "एकूण रक्कम": 5000, "दिनांक": "18/06/2016"}
    ])

if "deadstock" not in st.session_state:
    st.session_state.deadstock = pd.DataFrame([
        {"क्र.": 1, "साहित्य / वस्तू नाव": "कम्प्युटर सिस्टीम (HP i5)", "खरेदी दिनांक": "15/06/2021", "नग": 2, "मूळ किंमत": 95000, "घसारा %": 20, "घसारा रक्कम": 19000, "निव्वळ मूल्य": 76000},
        {"क्र.": 2, "साहित्य / वस्तू नाव": "ऑफिस लोखंडी तिजोरी", "खरेदी दिनांक": "10/05/2018", "नग": 1, "मूळ किंमत": 65000, "घसारा %": 5, "घसारा रक्कम": 3250, "निव्वळ मूल्य": 61750}
    ])

if "cashbook" not in st.session_state:
    st.session_state.cashbook = pd.DataFrame([
        {"तारीख": "30/03/2024", "व्हाऊचर क्र.": "VR-891", "तपशील": "सुरुवातीची हातशिल्लक", "शीर्षक": "Opening Balance", "जमा": 45000, "नावे": 0, "शिल्लक": 45000},
        {"तारीख": "30/03/2024", "व्हाऊचर क्र.": "RCT-142", "तपशील": "सुनील पाटील - हप्ता जमा", "शीर्षक": "कर्ज वसुली", "जमा": 12500, "नावे": 0, "शिल्लक": 57500}
    ])

if "audit_abc" not in st.session_state:
    st.session_state.audit_abc = pd.DataFrame([
        {"दोष क्र.": "DEF-1", "विभाग": "विभाग (अ) - गंभीर", "तपशील": "मृत सभासदाच्या खात्यावर वारस तपासणी पूर्ण नाही.", "रक्कम": 45000, "दुरुस्ती": "कायदेशीर संमतीपत्र घेऊन खाते नियमित करावे.", "स्थिती": "दुरुस्ती चालू"},
        {"दोष क्र.": "DEF-2", "विभाग": "विभाग (ब) - मध्यम", "तपशील": "कर्ज खाते क्र. १०४ मध्ये वाहन विम्याची चालू प्रत नाही.", "रक्कम": 0, "दुरुस्ती": "विमा पॉलिसी जमा करावी.", "स्थिती": "प्रलंबित"}
    ])

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
st.sidebar.title("🏛️ संस्था ऑडिट प्रणाली")
st.sidebar.caption("महाराष्ट्र सह. संस्था अधिनियम १९६० अंतर्गत")

menu = st.sidebar.radio(
    "मॉड्यूल निवडा:",
    [
        "१) नमुना क्र. ०१ (संस्था माहिती)",
        "२) नमुना क्र. ०८ (ऑडिट वर्गवारी)",
        "३) कलम ८१(२)(१) प्रतिज्ञापत्र",
        "४) कलम ८१(२) अन्वये १ ते ०९ बाबी",
        "५) विभाग (अ), (ब) आणि (क) दोष",
        "६) नमुना (M) / नमुना 'एम'",
        "७) तेहरीज, नफा-तोटा व ताळेबंद (Excel Upload)",
        "८) सभासद कर्ज यादी (Excel Upload)",
        "९) संचालक मंडळ यादी",
        "१०) भाग यादी (शेअर्स)",
        "११) डेडस्टॉक यादी",
        "१२) कॅश बूक (रोजकीर्द)",
        "★ एकत्रित ऑडिट अहवाल (Report View & PDF)"
    ]
)

# -------------------------------------------------------------
# 1. नमुना क्र. ०१
# -------------------------------------------------------------
if menu == "१) नमुना क्र. ०१ (संस्था माहिती)":
    st.header("📋 नमुना क्र. ०१ - संस्थेची प्राथमिक माहिती")
    with st.form("form_namuna_1"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("संस्थेचे संपूर्ण नाव", value=st.session_state.society["name"])
            reg_no = st.text_input("नोंदणी क्र. व दिनांक", value=st.session_state.society["reg_no"])
            address = st.text_input("पत्ता व कार्यक्षेत्र", value=st.session_state.society["address"])
            soc_type = st.text_input("संस्थेशी प्रकार", value=st.session_state.society["soc_type"])
        with col2:
            fin_year = st.text_input("आर्थिक वर्ष", value=st.session_state.society["fin_year"])
            members = st.number_input("एकूण सभासद संख्या", value=int(st.session_state.society["members"]))
            auditor = st.text_input("वैधानिक लेखापरीक्षकाचे नाव", value=st.session_state.society["auditor"])
            order_no = st.text_input("ऑडिट आदेश क्र.", value=st.session_state.society["order_no"])
        
        submitted = st.form_submit_button("💾 माहिती जतन करा")
        if submitted:
            st.session_state.society.update({
                "name": name, "reg_no": reg_no, "address": address, "soc_type": soc_type,
                "fin_year": fin_year, "members": members, "auditor": auditor, "order_no": order_no
            })
            st.success("नमुना क्र. ०१ माहिती यशस्वीरीत्या अपडेट केली!")

# -------------------------------------------------------------
# 2. नमुना क्र. ०८ (गुणांकन व वर्गवारी)
# -------------------------------------------------------------
elif menu == "२) नमुना क्र. ०८ (ऑडिट वर्गवारी)":
    st.header("🏆 नमुना क्र. ०८ - लेखापरीक्षण वर्गवारी व गुणांकन")
    st.caption("एकूण १०० गुणांनुसार ऑडिट वर्ग ('अ', 'ब', किंवा 'क') आपोआप निश्चित केला जातो.")
    
    col1, col2 = st.columns(2)
    with col1:
        m1 = st.slider("१. भागभांडवल व निधी वाढ आणि आर्थिक सुरक्षितता (कमाल १५)", 0, 15, 13)
        m2 = st.slider("२. ठेव संकलन व आर्थिक स्त्रोत वाढ (कमाल १५)", 0, 15, 13)
        m3 = st.slider("३. कर्ज वाटप, नियमपालन व तारण सुरक्षितता (कमाल २०)", 0, 20, 17)
    with col2:
        m4 = st.slider("४. कर्ज वसुली व NPA प्रमाण (कमाल २०)", 0, 20, 16)
        m5 = st.slider("५. दैनिक हिशोब, रोजकीर्द, खतावणी पूर्णता (कमाल १५)", 0, 15, 14)
        m6 = st.slider("६. व्यवस्थापन, संचालक सभा व कायदेपालन (कमाल १५)", 0, 15, 13)
        
    total_marks = m1 + m2 + m3 + m4 + m5 + m6
    if total_marks >= 70:
        audit_grade = "'अ' वर्ग (A Class)"
    elif total_marks >= 55:
        audit_grade = "'ब' वर्ग (B Class)"
    else:
        audit_grade = "'क' वर्ग (C Class)"
        
    st.session_state.society["audit_class"] = audit_grade
    st.metric(label="एकूण मिळालेले गुण (Total Marks)", value=f"{total_marks} / १००", delta=audit_grade)

# -------------------------------------------------------------
# 3. कलम ८१(२)(१) प्रतिज्ञापत्र
# -------------------------------------------------------------
elif menu == "३) कलम ८१(२)(१) प्रतिज्ञापत्र":
    st.header("📜 कलम ८१(२)(१) प्रमाणे वैधानिक लेखापरीक्षक प्रतिज्ञापत्र")
    affidavit_text = f"""
    मी/आम्ही, खालील स्वाक्षरी करणारे वैधानिक लेखापरीक्षक याद्वारे प्रतिज्ञापत्रावर लिहून देतो की —
    
    १. आम्ही *{st.session_state.society['name']}* या संस्थेचे सन *{st.session_state.society['fin_year']}* या वर्षाचे वैधानिक लेखापरीक्षण स्वतः पूर्ण केलेले आहे.
    २. लेखापरीक्षणादरम्यान आवश्यक असणारी सर्व पुस्तके, व्हाऊचर्स, कर्ज प्रकरणे, बँक स्टेटमेंट व इतर कागदपत्रे संस्थेने तपासणीसाठी उपलब्ध करून दिली होती.
    ३. आमच्या समजुतीनुसार व आम्हाला दिलेल्या माहितीनुसार संस्थेचे आर्थिक पत्रके, ताळेबंद व नफा-तोटा हिशोब संस्थेच्या आर्थिक व्यवहारांचे खरे आणि वस्तुनिष्ठ (True and Fair) चित्रण दर्शवितात.
    ४. निधीचा कोणताही गैरवापर किंवा अपहार आढळल्यास त्याचा स्वतंत्र उल्लेख दोष दुरुस्ती यादीत केला आहे.
    """
    st.info(affidavit_text)
    col1, col2 = st.columns(2)
    with col1:
        st.write("ठिकाण: *लातूर / कोल्हापूर*")
        st.write("दिनांक: *31/07/2024*")
    with col2:
        st.write(f"*{st.session_state.society['auditor']}*")
        st.caption("वैधानिक लेखापरीक्षक (शिक्का व स्वाक्षरी)")

# -------------------------------------------------------------
# 4. कलम ८१(२) अन्वये १ ते ०९ बाबी
# -------------------------------------------------------------
elif menu == "४) कलम ८१(२) अन्वये १ ते ०९ बाबी":
    st.header("⚖️ कलम ८१(२) अन्वये १ ते ०९ मुद्द्यांची अभिप्रेत माहिती")
    clauses = [
        ("१. कर्ज व अग्रिमांची सुरक्षितता", "संस्थेने वितरित केलेली कर्जे पुरेसे तारण, जामीनदार व कागदपत्रांसह सुरक्षित आहेत."),
        ("२. संस्थेच्या हितावर परिणाम करणारे व्यवहार", "सर्व व्यवहार प्रत्यक्ष झालेले असून निव्वळ पुस्तकी नोंदी करून कोणताही व्यवहार केलेला नाही."),
        ("३. वैयक्तिक खर्चाची नोंद", "संचालक अथवा कर्मचाऱ्यांचे वैयक्तिक खर्च महसुली खर्चात खर्ची टाकलेले नाहीत."),
        ("४. वित्तीय अनियमितता व निधी अपहार", "लेखापरीक्षणादरम्यान कोणत्याही प्रकारचा अपहार अथवा गैरव्यवहार निदर्शनास आलेला नाही."),
        ("५. उपविधी, कायदा व नियमांचे उल्लंघन", "कामकाज महाराष्ट्र सहकारी संस्था अधिनियम १९६० व उपविधीनुसार चालत आहे."),
        ("६. संचालक मंडळ कर्ज मर्यादा व दायित्व", "संचालक मंडळाकडील कर्जे उपविधीतील मर्यादेत असून परतफेड नियमित आहे."),
        ("७. थकीत व संशयित कर्ज तरतूद (BDDR)", "निकषांनुसार संशयित कर्ज निधी (BDDR) साठी पुरेशी तरतूद नफा-तोटा खात्यातून केलेली आहे."),
        ("८. गुंतवणूक व शासकीय रोखे सुरक्षितता", "गुंतवणूक जिल्हा मध्यवर्ती सहकारी बँकेत सुरक्षित आहे."),
        ("९. मागील ऑडिट दोषांची पूर्तता", "मागील वर्षाच्या ऑडिट दोषांची पूर्तता करून 'नमुना ओ' मुदतीत निबंधकांकडे पाठविला आहे.")
    ]
    for title, default_val in clauses:
        st.text_area(title, value=default_val, height=70)

# -------------------------------------------------------------
# 5. विभाग (अ), (ब) आणि (क) दोष
# -------------------------------------------------------------
elif menu == "५) विभाग (अ), (ब) आणि (क) दोष":
    st.header("🔍 लेखापरीक्षण दोष दुरुस्ती विभाग (अ), (ब) आणि (क)")
    st.dataframe(st.session_state.audit_abc, use_container_width=True)
    
    with st.expander("+ नवीन दोष नोंदवा"):
        with st.form("form_add_fault"):
            f_sec = st.selectbox("दोष विभाग निवडा", ["विभाग (अ) - गंभीर", "विभाग (ब) - मध्यम", "विभाग (क) - किरकोळ"])
            f_desc = st.text_area("दोषाचा तपशील")
            f_amt = st.number_input("संबंधित रक्कम (₹)", value=0)
            f_rem = st.text_area("संस्थेने करावयाची दुरुस्ती / उपाययोजना")
            f_stat = st.selectbox("स्थिती", ["प्रलंबित", "दुरुस्ती चालू", "दुरुस्त झाले"])
            
            if st.form_submit_button("जतन करा"):
                new_f = {
                    "दोष क्र.": f"DEF-{len(st.session_state.audit_abc) + 1}",
                    "विभाग": f_sec, "तपशील": f_desc, "रक्कम": f_amt,
                    "दुरुस्ती": f_rem, "स्थिती": f_stat
                }
                st.session_state.audit_abc = pd.concat([st.session_state.audit_abc, pd.DataFrame([new_f])], ignore_index=True)
                st.success("दोष यशस्वीरीत्या नोंदवला!")
                st.rerun()

# -------------------------------------------------------------
# 6. नमुना (M) / नमुना 'एम'
# -------------------------------------------------------------
elif menu == "६) नमुना (M) / नमुना 'एम'":
    st.header("📊 नमुना 'एम' (Form M) - वित्तीय सारांश पत्रक")
    df_m = pd.DataFrame([
        {"घटक / बाब": "वसूल भागभांडवल", "चालू वर्ष (₹)": 1520000, "मागील वर्ष (₹)": 1380000, "शेरा": "+10.1% वाढ"},
        {"घटक / बाब": "राखीव व इतर निधी", "चालू वर्ष (₹)": 660000, "मागील वर्ष (₹)": 590000, "शेरा": "निधी वाढ"},
        {"घटक / बाब": "एकूण ठेवी", "चालू वर्ष (₹)": 3850000, "मागील वर्ष (₹)": 3410000, "शेरा": "समाधानकारक"},
        {"घटक / बाब": "कर्ज वाटप येणे", "चालू वर्ष (₹)": 4850000, "मागील वर्ष (₹)": 4200000, "शेरा": "नियमित वसुली"},
        {"घटक / बाब": "एकूण थकबाकी", "चालू वर्ष (₹)": 340000, "मागील वर्ष (₹)": 410000, "शेरा": "थकबाकी घट (उत्तम)"},
        {"घटक / बाब": "निव्वळ नफा", "चालू वर्ष (₹)": 385000, "मागील वर्ष (₹)": 330000, "शेरा": "१६.६% नफा वाढ"}
    ])
    st.dataframe(df_m, use_container_width=True)

# -------------------------------------------------------------
# 7. तेहरीज, नफा-तोटा व ताळेबंद (With Excel Upload)
# -------------------------------------------------------------
elif menu == "७) तेहरीज, नफा-तोटा व ताळेबंद (Excel Upload)":
    st.header("📑 तेहरीज, नफा-तोटा पत्रक व ताळेबंद")
    
    st.markdown("### 📥 Excel अपलोड व टेम्पलेट")
    col_up1, col_up2 = st.columns(2)
    
    with col_up1:
        template_df = pd.DataFrame([
            {"बाजू": "देयता", "तपशील": "भाग भांडवल", "रक्कम": 1520000},
            {"बाजू": "देयता", "तपशील": "ठेवी", "रक्कम": 3850000},
            {"बाजू": "मालमत्ता", "तपशील": "कर्ज येणे बाकी", "रक्कम": 4850000},
            {"बाजू": "मालमत्ता", "तपशील": "बँक शिल्लक", "रक्कम": 242000}
        ])
        buffer = io.BytesIO()
        template_df.to_excel(buffer, index=False)
        st.download_button("📥 तेहरीज Excel Template डाऊनलोड", data=buffer.getvalue(), file_name="teharij_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    with col_up2:
        uploaded_teharij = st.file_uploader("📊 तेहरीज Excel फाईल निवडा (.xlsx)", type=["xlsx", "csv"], key="teharij_file")
        if uploaded_teharij:
            try:
                df_up = pd.read_excel(uploaded_teharij) if uploaded_teharij.name.endswith('.xlsx') else pd.read_csv(uploaded_teharij)
                liab = df_up[df_up["बाजू"].str.contains("देयता|जमा|Liab", case=False, na=False)][["तपशील", "रक्कम"]]
                assets = df_up[df_up["बाजू"].str.contains("मालमत्ता|नावे|Asset", case=False, na=False)][["तपशील", "रक्कम"]]
                if not liab.empty: st.session_state.teharij_liab = liab
                if not assets.empty: st.session_state.teharij_assets = assets
                st.success("तेहरीज व ताळेबंद एक्सेलवरून यशस्वीरीत्या आयात झाले!")
            except Exception as e:
                st.error(f"एरर: {e}")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("देयता बाजू (Liabilities)")
        st.dataframe(st.session_state.teharij_liab, use_container_width=True)
        st.metric("एकूण देयता (Total)", f"₹ {st.session_state.teharij_liab['रक्कम'].sum():,}")
    with c2:
        st.subheader("मालमत्ता बाजू (Assets)")
        st.dataframe(st.session_state.teharij_assets, use_container_width=True)
        st.metric("एकूण मालमत्ता (Total)", f"₹ {st.session_state.teharij_assets['रक्कम'].sum():,}")

# -------------------------------------------------------------
# 8. सभासद कर्ज यादी (With Excel Upload)
# -------------------------------------------------------------
elif menu == "८) सभासद कर्ज यादी (Excel Upload)":
    st.header("👥 सभासद कर्ज यादी व वर्गवारी")
    
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        loan_tmpl = pd.DataFrame([
            {"खाते क्र.": "101", "सभासदाचे नाव": "सुनील पाटील", "कर्ज प्रकार": "तारण कर्ज", "मंजूर दिनांक": "15/04/2023", "मंजूर रक्कम": 300000, "शिल्लक मुद्दल": 210000, "थकीत रक्कम": 0, "स्थिती": "नियमित"}
        ])
        buf_l = io.BytesIO()
        loan_tmpl.to_excel(buf_l, index=False)
        st.download_button("📥 कर्ज यादी Template", data=buf_l.getvalue(), file_name="loan_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    with col_l2:
        up_loan = st.file_uploader("📊 कर्ज यादी Excel अपलोड करा", type=["xlsx", "csv"], key="loan_file")
        if up_loan:
            try:
                df_l = pd.read_excel(up_loan) if up_loan.name.endswith('.xlsx') else pd.read_csv(up_loan)
                st.session_state.loans = df_l
                st.success(f"{len(df_l)} कर्ज खाती यशस्वीरीत्या जोडली!")
            except Exception as e:
                st.error(f"एरर: {e}")
                
    with col_l3:
        buf_exp = io.BytesIO()
        st.session_state.loans.to_excel(buf_exp, index=False)
        st.download_button("📤 चालू यादी Excel डाऊनलोड", data=buf_exp.getvalue(), file_name="current_loan_list.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.dataframe(st.session_state.loans, use_container_width=True)
    
    with st.expander("+ नवीन कर्ज खाते नोंदवा"):
        with st.form("form_add_loan"):
            col_a, col_b = st.columns(2)
            with col_a:
                l_ac = st.text_input("खाते क्र.", value=f"10{len(st.session_state.loans)+1}")
                l_name = st.text_input("सभासदाचे नाव")
                l_type = st.selectbox("कर्ज प्रकार", ["तारण कर्ज", "वैयक्तिक कर्ज", "व्यापार कर्ज", "वाहन कर्ज"])
                l_date = st.text_input("मंजूर दिनांक", "01/03/2024")
            with col_b:
                l_sanc = st.number_input("मंजूर रक्कम (₹)", value=100000)
                l_bal = st.number_input("शिल्लक मुद्दल (₹)", value=90000)
                l_ovd = st.number_input("थकीत रक्कम (₹)", value=0)
                l_st = st.selectbox("स्थिती", ["नियमित", "मध्यम थकबाकी", "गंभीर थकबाकी"])
            
            if st.form_submit_button("कर्ज जतन करा"):
                if l_name:
                    new_l = {"खाते क्र.": l_ac, "सभासदाचे नाव": l_name, "कर्ज प्रकार": l_type, "मंजूर दिनांक": l_date, "मंजूर रक्कम": l_sanc, "शिल्लक मुद्दल": l_bal, "थकीत रक्कम": l_ovd, "स्थिती": l_st}
                    st.session_state.loans = pd.concat([st.session_state.loans, pd.DataFrame([new_l])], ignore_index=True)
                    st.success("नोंद झाली!")
                    st.rerun()

# -------------------------------------------------------------
# 9. संचालक मंडळ यादी
# -------------------------------------------------------------
elif menu == "९) संचालक मंडळ यादी":
    st.header("👔 संचालक मंडळ यादी (Board of Directors)")
    st.dataframe(st.session_state.directors, use_container_width=True)
    with st.expander("+ नवीन संचालक जोडा"):
        with st.form("form_add_dir"):
            d_name = st.text_input("संचालकाचे नाव")
            d_role = st.text_input("पद", "संचालक")
            d_term = st.text_input("कालावधी", "2021-2026")
            d_loan = st.number_input("संस्थेकडील कर्ज (₹)", value=0)
            d_att = st.text_input("हजेरी %", "90%")
            d_rem = st.text_input("शेरा", "पात्र")
            if st.form_submit_button("संचालक जोडा"):
                if d_name:
                    new_d = {"अ.क्र.": len(st.session_state.directors)+1, "संचालकाचे नाव": d_name, "पद / हुद्दा": d_role, "मुदत": d_term, "संस्थेकडील कर्ज": d_loan, "हजेरी %": d_att, "शेरा": d_rem}
                    st.session_state.directors = pd.concat([st.session_state.directors, pd.DataFrame([new_d])], ignore_index=True)
                    st.success("संचालक जोडले!")
                    st.rerun()

# -------------------------------------------------------------
# 10. भाग यादी
# -------------------------------------------------------------
elif menu == "१०) भाग यादी (शेअर्स)":
    st.header("🏷️ भाग भांडवल यादी (Share Capital Register)")
    st.dataframe(st.session_state.shares, use_container_width=True)

# -------------------------------------------------------------
# 11. डेडस्टॉक यादी
# -------------------------------------------------------------
elif menu == "११) डेडस्टॉक यादी":
    st.header("🪑 डेडस्टॉक व फर्निचर यादी")
    st.dataframe(st.session_state.deadstock, use_container_width=True)

# -------------------------------------------------------------
# 12. कॅश बूक
# -------------------------------------------------------------
elif menu == "१२) कॅश बूक (रोजकीर्द)":
    st.header("📖 दैनिक कॅश बूक (रोजकीर्द)")
    st.dataframe(st.session_state.cashbook, use_container_width=True)

# -------------------------------------------------------------
# ★ Report View & PDF Download
# -------------------------------------------------------------
elif menu == "★ एकत्रित ऑडिट अहवाल (Report View & PDF)":
    st.header("📑 एकत्रित वैधानिक लेखापरीक्षण अहवाल")
    st.markdown(f"""
    ### *{st.session_state.society['name']}*
    *नोंदणी क्र.:* {st.session_state.society['reg_no']} | *कार्यक्षेत्र:* {st.session_state.society['address']}  
    *आर्थिक वर्ष:* {st.session_state.society['fin_year']} | *घोषित ऑडिट वर्ग:* :green[*{st.session_state.society['audit_class']}*]
    
    ---
    #### १. आर्थिक ताळेबंद स्थिती (Summary)
    * *एकूण देयता (Liabilities):* ₹ {st.session_state.teharij_liab['रक्कम'].sum():,}
    * *एकूण मालमत्ता (Assets):* ₹ {st.session_state.teharij_assets['रक्कम'].sum():,}
    * *एकूण सभासद कर्ज बाकी:* ₹ {st.session_state.loans['शिल्लक मुद्दल'].sum():,}
    * *एकूण थकीत कर्ज रक्कम:* ₹ {st.session_state.loans['थकीत रक्कम'].sum():,}
    
    #### २. वैधानिक लेखापरीक्षक शेरा
    संस्थेचे हिशोब तपासणीअंती समाधानकारक असून महाराष्ट्र सहकारी संस्था अधिनियम १९६० व उपविधीनुसार व्यवहार झालेले आहेत.
    """)

    st.markdown("---")
    st.subheader("🖨️ अधिकृत वैधानिक ऑडिट अहवाल PDF डाऊनलोड करा")
    
    if st.button("🚀 संपूर्ण ३०-४० पानांचा अहवाल PDF जनरेट करा", type="primary"):
        with st.spinner("PDF अहवाल तयार होत आहे..."):
            try:
                env = Environment(loader=FileSystemLoader("templates"))
                template = env.get_template("final_accounts.html")
                
                rendered_html = template.render(
                    sanstha_name=st.session_state.society["name"],
                    reg_no=st.session_state.society["reg_no"],
                    address=st.session_state.society["address"],
                    fin_year=st.session_state.society["fin_year"],
                    audit_class=st.session_state.society["audit_class"],
                    auditor_name=st.session_state.society["auditor"],
                    liabilities=st.session_state.teharij_liab.to_dict(orient='records'),
                    assets=st.session_state.teharij_assets.to_dict(orient='records'),
                    loans=st.session_state.loans.to_dict(orient='records'),
                    directors=st.session_state.directors.to_dict(orient='records'),
                    shares=st.session_state.shares.to_dict(orient='records'),
                    deadstock=st.session_state.deadstock.to_dict(orient='records'),
                    cashbook=st.session_state.cashbook.to_dict(orient='records'),
                    audit_abc=st.session_state.audit_abc.to_dict(orient='records')
                )
                
                pdf_bytes = HTML(string=rendered_html).write_pdf()
                
                st.success("अहवाल यशस्वीरीत्या तयार झाला!")
                st.download_button(
                    label="📥 डाऊनलोड संपूर्ण वैधानिक ऑडिट अहवाल (PDF)",
                    data=pdf_bytes,
                    file_name=f"Full_Statutory_Audit_{st.session_state.society['name'][:15]}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF तयार करताना त्रुटी आली: {str(e)}")
