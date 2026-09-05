import streamlit as st
import pandas as pd
import io
from weasyprint import HTML
from jinja2 import Template

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
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
        "name": "पशुवैद्यकीय महाविद्यालय कर्मचारी सहकारी पतसंस्था मर्यादित, उदगीर",
        "reg_no": "LTR/UGR/RSR/CR/940/2001 दि. 11.05.2001",
        "address": "पशुवैद्यकीय महाविद्यालय, उदगीर ता. उदगीर जि. लातूर",
        "taluka": "उदगीर",
        "district": "लातूर",
        "fin_year": "2025-2026 (दि. ०१/०४/२०२५ ते ३१/०३/२०२६)",
        "soc_type": "वेतनदारांची सहकारी पतसंस्था मर्यादित",
        "area_operation": "महाविद्यालय कर्मचाऱ्यांपुरते मर्यादित",
        "members": 82,
        "auditor": "विनोद एस. पटवारी",
        "auditor_desig": "प्रमाणित लेखापरीक्षक, उदगीर (नों. क्र. ९९०९९)",
        "order_no": "DDR/LTR/AUDIT/ORDER/2026 दि. 15/05/2026",
        "audit_class": "'अ' वर्ग (A Class)",
        "last_3_years_class": "अ, अ, अ",
        "audit_period": "दि. ०१/०४/२०२५ ते ३१/०३/२०२६",
        "audit_start_date": "06/06/2026",
        "audit_end_date": "10/06/2026",
        "audit_submit_date": "02/07/2026"
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
        {"खाते क्र.": "101", "सभासदाचे नाव": "सुनील मारुती पाटील", "कर्ज प्रकार": "तारण कर्ज", "मंजूर दिनांक": "15/04/2025", "मंजूर रक्कम": 300000, "शिल्लक मुद्दल": 210000, "थकीत रक्कम": 0, "स्थिती": "नियमित"},
        {"खाते क्र.": "102", "सभासदाचे नाव": "तानाजी विठ्ठल शिंदे", "कर्ज प्रकार": "वैयक्तिक कर्ज", "मंजूर दिनांक": "10/06/2025", "मंजूर रक्कम": 150000, "शिल्लक मुद्दल": 95000, "थकीत रक्कम": 15000, "स्थिती": "मध्यम थकबाकी"},
        {"खाते क्र.": "103", "सभासदाचे नाव": "रमेश बापूराव देशमुख", "कर्ज प्रकार": "व्यापार कर्ज", "मंजूर दिनांक": "22/07/2025", "मंजूर रक्कम": 500000, "शिल्लक मुद्दल": 420000, "थकीत रक्कम": 0, "स्थिती": "नियमित"}
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
        {"तारीख": "30/03/2026", "व्हाऊचर क्र.": "VR-891", "तपशील": "सुरुवातीची हातशिल्लक", "शीर्षक": "Opening Balance", "जमा": 45000, "नावे": 0, "शिल्लक": 45000},
        {"तारीख": "30/03/2026", "व्हाऊचर क्र.": "RCT-142", "तपशील": "सुनील पाटील - हप्ता जमा", "शीर्षक": "कर्ज वसुली", "जमा": 12500, "नावे": 0, "शिल्लक": 57500}
    ])

if "audit_abc" not in st.session_state:
    st.session_state.audit_abc = pd.DataFrame([
        {"दोष क्र.": "१ (अ)", "विभाग": "विभाग (अ) - गंभीर", "तपशील": "काही खर्चाच्या व्हाऊचर्सवर व्यवस्थापकांची स्वाक्षरी प्रलंबित होती.", "रक्कम": 45000, "दुरुस्ती": "सदर व्हाऊचर्सवर आवश्यक त्या स्वाक्षऱ्या घेण्यात आल्या.", "स्थिती": "दुरुस्त झाले"},
        {"दोष क्र.": "२ (ब)", "विभाग": "विभाग (ब) - मध्यम", "तपशील": "३१ मार्च अखेरचे बँक मेळ जुळवणी पत्रक (BRS) उपलब्ध नव्हते.", "रक्कम": 0, "दुरुस्ती": "सर्व बँकांचे मार्च अखेरचे BRS तयार करून फाईल करण्यात आले.", "स्थिती": "दुरुस्त झाले"}
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
            soc_type = st.text_input("संस्थेचा प्रकार", value=st.session_state.society["soc_type"])
            taluka = st.text_input("तालुका", value=st.session_state.society["taluka"])
            district = st.text_input("जिल्हा", value=st.session_state.society["district"])
        with col2:
            fin_year = st.text_input("आर्थिक वर्ष", value=st.session_state.society["fin_year"])
            members = st.number_input("एकूण सभासद संख्या", value=int(st.session_state.society["members"]))
            auditor = st.text_input("वैधानिक लेखापरीक्षकाचे नाव", value=st.session_state.society["auditor"])
            auditor_desig = st.text_input("लेखापरीक्षक पदनाम / पत्ता", value=st.session_state.society["auditor_desig"])
            order_no = st.text_input("ऑडिट आदेश क्र.", value=st.session_state.society["order_no"])
        
        submitted = st.form_submit_button("💾 माहिती जतन करा")
        if submitted:
            st.session_state.society.update({
                "name": name, "reg_no": reg_no, "address": address, "soc_type": soc_type,
                "taluka": taluka, "district": district, "fin_year": fin_year, "members": members,
                "auditor": auditor, "auditor_desig": auditor_desig, "order_no": order_no
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
        st.write(f"ठिकाण: *{st.session_state.society['taluka']}*")
        st.write(f"दिनांक: *{st.session_state.society['audit_submit_date']}*")
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
                    "दोष क्र.": f"{len(st.session_state.audit_abc) + 1} ({f_sec[7]})",
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
# 7. तेहरीज, नफा-तोटा व ताळेबंद (Smart Excel Upload - No Error)
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
                
                # ऑटो-डिटेक्ट: 'बाजू' कॉलम असल्यास किंवा जुन्या 'Type' कॉलम असल्यास
                if "बाजू" in df_up.columns:
                    liab = df_up[df_up["बाजू"].astype(str).str.contains("देयता|जमा|Liab", case=False, na=False)][["तपशील", "रक्कम"]]
                    assets = df_up[df_up["बाजू"].astype(str).str.contains("मालमत्ता|नावे|Asset", case=False, na=False)][["तपशील", "रक्कम"]]
                elif "Type" in df_up.columns:
                    col_name = "खात्याचे नाव" if "खात्याचे नाव" in df_up.columns else df_up.columns[0]
                    credit_col = 'Credit' if 'Credit' in df_up.columns else df_up.columns[3]
                    debit_col = 'Debit' if 'Debit' in df_up.columns else df_up.columns[2]
                    
                    df_up['रक्कम'] = df_up.apply(lambda r: r.get(credit_col, 0) if r['Type'] in ['Liability', 'Income'] else r.get(debit_col, 0), axis=1)
                    liab = df_up[df_up["Type"].astype(str).str.contains("Liability|Income", case=False, na=False)][[col_name, "रक्कम"]].rename(columns={col_name: "तपशील"})
                    assets = df_up[df_up["Type"].astype(str).str.contains("Asset|Expense", case=False, na=False)][[col_name, "रक्कम"]].rename(columns={col_name: "तपशील"})
                else:
                    # तिसरा पर्याय: जर कॉलम १ तपशील आणि कॉलम २ रक्कम असेल तर
                    liab = df_up.iloc[:len(df_up)//2, :2]
                    liab.columns = ["तपशील", "रक्कम"]
                    assets = df_up.iloc[len(df_up)//2:, :2]
                    assets.columns = ["तपशील", "रक्कम"]

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
        st.metric("एकूण देयता (Total)", f"₹ {int(st.session_state.teharij_liab['रक्कम'].sum()):,}")
    with c2:
        st.subheader("मालमत्ता बाजू (Assets)")
        st.dataframe(st.session_state.teharij_assets, use_container_width=True)
        st.metric("एकूण मालमत्ता (Total)", f"₹ {int(st.session_state.teharij_assets['रक्कम'].sum()):,}")

# -------------------------------------------------------------
# 8. सभासद कर्ज यादी (With Excel Upload)
# -------------------------------------------------------------
elif menu == "८) सभासद कर्ज यादी (Excel Upload)":
    st.header("👥 सभासद कर्ज यादी व वर्गवारी")
    
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        loan_tmpl = pd.DataFrame([
            {"खाते क्र.": "101", "सभासदाचे नाव": "सुनील पाटील", "कर्ज प्रकार": "तारण कर्ज", "मंजूर दिनांक": "15/04/2025", "मंजूर रक्कम": 300000, "शिल्लक मुद्दल": 210000, "थकीत रक्कम": 0, "स्थिती": "नियमित"}
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

# -------------------------------------------------------------
# 9. संचालक मंडळ यादी
# -------------------------------------------------------------
elif menu == "९) संचालक मंडळ यादी":
    st.header("👔 संचालक मंडळ यादी (Board of Directors)")
    st.dataframe(st.session_state.directors, use_container_width=True)

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
# ★ एकत्रित ऑडिट अहवाल (PDF Generator)
# -------------------------------------------------------------
elif menu == "★ एकत्रित ऑडिट अहवाल (Report View & PDF)":
    st.header("📑 एकत्रित वैधानिक लेखापरीक्षण अहवाल")
    st.markdown(f"""
    ### *{st.session_state.society['name']}*
    *नोंदणी क्र.:* {st.session_state.society['reg_no']} | *कार्यक्षेत्र:* {st.session_state.society['address']}  
    *आर्थिक वर्ष:* {st.session_state.society['fin_year']} | *घोषित ऑडिट वर्ग:* :green[*{st.session_state.society['audit_class']}*]
    
    ---
    #### १. आर्थिक ताळेबंद स्थिती (Summary)
    * *एकूण देयता (Liabilities):* ₹ {int(st.session_state.teharij_liab['रक्कम'].sum()):,}
    * *एकूण मालमत्ता (Assets):* ₹ {int(st.session_state.teharij_assets['रक्कम'].sum()):,}
    * *एकूण सभासद कर्ज बाकी:* ₹ {int(st.session_state.loans['शिल्लक मुद्दल'].sum()):,}
    * *एकूण थकीत कर्ज रक्कम:* ₹ {int(st.session_state.loans['थकीत रक्कम'].sum()):,}
    
    #### २. वैधानिक लेखापरीक्षक शेरा
    संस्थेचे हिशोब तपासणीअंती समाधानकारक असून महाराष्ट्र सहकारी संस्था अधिनियम १९६० व उपविधीनुसार व्यवहार झालेले आहेत.
    """)

    st.markdown("---")
    st.subheader("🖨️ अधिकृत वैधानिक ऑडिट अहवाल PDF डाऊनलोड करा")
    
    if st.button("🚀 संपूर्ण वैधानिक अहवाल (सर्व विभागांसह) PDF जनरेट करा", type="primary"):
        with st.spinner("संपूर्ण ३०-४० पानांचा अहवाल PDF मध्ये संकलित होत आहे..."):
            try:
                # इनलाइन HTML टेम्पलेट - संपूर्ण अहवाल एकाच ठिकाणी
                full_html_template = """
                <!DOCTYPE html>
                <html lang="mr">
                <head>
                <meta charset="UTF-8">
                <style>
                  @page {
                    size: A4 portrait;
                    margin: 15mm 12mm 15mm 12mm;
                    @top-center {
                      content: "{{ soc.name }} - वैधानिक लेखापरीक्षण अहवाल ({{ soc.fin_year }})";
                      font-size: 8px;
                      border-bottom: 1px solid #aaa;
                    }
                    @bottom-right {
                      content: "पान क्र. " counter(page);
                      font-size: 8px;
                    }
                  }
                  body {
                    font-family: 'Noto Sans Devanagari', Arial, sans-serif;
                    font-size: 10.5px;
                    line-height: 1.25;
                    color: #000;
                  }
                  .page-break { page-break-after: always; }
                  .header { text-align: center; margin-bottom: 12px; }
                  .header h2 { margin: 2px 0; font-size: 15px; }
                  .header h3 { margin: 2px 0; font-size: 12px; }
                  .header p { margin: 1px 0; font-size: 10px; }
                  .section-title {
                    background-color: #f2f2f2;
                    font-weight: bold;
                    padding: 4px 6px;
                    border: 1px solid #000;
                    margin-top: 10px;
                    margin-bottom: 4px;
                    font-size: 11px;
                  }
                  table { width: 100%; border-collapse: collapse; margin-bottom: 10px; }
                  th, td { border: 1px solid #000; padding: 4px 6px; }
                  th { background-color: #f7f7f7; text-align: center; }
                  .text-right { text-align: right; }
                  .text-center { text-align: center; }
                  .sign-container { margin-top: 25px; width: 100%; display: flex; }
                  .sign-box { width: 50%; float: left; text-align: center; font-size: 10px; }
                </style>
                </head>
                <body>

                <!-- पान १: नमुना क्रमांक १ : विभाग पहिला -->
                <div class="header">
                  <p style="font-size: 13px; font-weight: bold;">नमुना क्रमांक :- १</p>
                  <h2>लेखापरीक्षा अहवाल (सर्व सहकारी संस्थांसाठी)</h2>
                  <h3>विभाग - पहिला (सामान्य व प्रशासकीय माहिती)</h3>
                </div>

                <table style="border:none;">
                  <tr>
                    <td style="width: 60%; border:none; vertical-align: top;">
                      <strong>संस्थेचे नाव:</strong> {{ soc.name }}<br>
                      <strong>नोंदलेला संपूर्ण पत्ता:</strong> {{ soc.address }}<br>
                      <strong>तालुका / गट:</strong> {{ soc.taluka }} | <strong>जि.:</strong> {{ soc.district }}<br>
                      <strong>नोंदणी क्रमांक व दिनांक:</strong> {{ soc.reg_no }}<br>
                      <strong>संस्थेचे कार्यक्षेत्र:</strong> {{ soc.area_operation }}
                    </td>
                    <td style="width: 40%; border:none; vertical-align: top;">
                      <strong>लेखापरीक्षण नोंदवही अ.क्र.:</strong> ९९०९९<br>
                      <strong>चालू लेखापरीक्षण वर्गीकरण:</strong> {{ soc.audit_class }}<br>
                      <strong>गेल्या ३ वर्षांचे वर्ग:</strong> {{ soc.last_3_years_class }}
                    </td>
                  </tr>
                </table>

                <div class="section-title">१) लेखापरीक्षा विषयक माहिती</div>
                <table>
                  <tr>
                    <td style="width: 65%;">१) लेखापरीक्षा करणाऱ्या अधिकाऱ्याचे पूर्ण नाव, पदनाम व मुख्यालय</td>
                    <td style="width: 35%;">{{ soc.auditor }} ({{ soc.auditor_desig }})</td>
                  </tr>
                  <tr>
                    <td>२) चालू लेखापरीक्षेत समाविष्ट कालावधी</td>
                    <td>{{ soc.audit_period }}</td>
                  </tr>
                  <tr>
                    <td>३) लेखापरीक्षा सुरू व संपल्याचा दिनांक</td>
                    <td>दि. {{ soc.audit_start_date }} ते दि. {{ soc.audit_end_date }}</td>
                  </tr>
                  <tr>
                    <td>४) लेखापरीक्षा अहवाल सादर केल्याचा दिनांक</td>
                    <td>दि. {{ soc.audit_submit_date }}</td>
                  </tr>
                </table>

                <div class="section-title">२) सभासदत्व व भागभांडवल</div>
                <table>
                  <tr>
                    <td style="width: 65%;">१) एकूण सभासद संख्या (सर्वसाधारण)</td>
                    <td style="width: 35%;">{{ soc.members }}</td>
                  </tr>
                  <tr>
                    <td>२) 'आय' व 'जे' नमुन्यात सभासद नोंदवही अद्ययावत ठेवली आहे काय?</td>
                    <td>होय, पण काही नोंदी अपूर्ण स्थितीत आहेत</td>
                  </tr>
                  <tr>
                    <td>३) भागाची खतावणी अद्ययावत लिहून ताळेबंदाशी जुळते काय?</td>
                    <td>होय, जुळते</td>
                  </tr>
                  <tr>
                    <td>४) बाहेरील कर्ज मर्यादा काय ठरविली आहे? उल्लंघन झाले आहे काय?</td>
                    <td>भागभांडवल + राखीव निधीच्या १० पट (उल्लंघन नाही)</td>
                  </tr>
                </table>

                <div class="section-title">३) सभा व इतर माहिती</div>
                <table>
                  <tr>
                    <td style="width: 65%;">१) वार्षिक सर्वसाधारण सभा (AGM) दिनांक</td>
                    <td style="width: 35%;">दि. २५/०९/२०२५</td>
                  </tr>
                  <tr>
                    <td>२) व्यवस्थापक समिती / संचालक मंडळ सभा संख्या</td>
                    <td>एकूण १२ सभा</td>
                  </tr>
                  <tr>
                    <td>३) मागील लेखापरीक्षण दोष दुरुस्ती अहवाल (Form 'O') पाठविला आहे काय?</td>
                    <td>होय, पाठविला आहे</td>
                  </tr>
                </table>

                <div class="page-break"></div>

                <!-- पान २: नमुना क्र. ३ : विभाग दुसरा (वेतनदार पतसंस्था) -->
                <div class="header">
                  <p style="font-size: 13px; font-weight: bold;">नमुना क्र. ३</p>
                  <h2>लेखापरीक्षा अहवाल (वेतनदारांच्या सहकारी संस्था)</h2>
                  <h3>विभाग दुसरा : ठेवी, कर्जे, गुंतवणूक व व्यवसाय</h3>
                </div>

                <div class="section-title">१) ठेवी व चल संपत्ती</div>
                <table>
                  <tr>
                    <td style="width: 70%;">अ) वेतनातून ठेवी/वर्गण्यांची पोटनियमानुसार काटेकोर कपात होते काय?</td>
                    <td style="width: 30%;">होय</td>
                  </tr>
                  <tr>
                    <td>ब) वर्गण्यांचे नियमितपणे भागात रूपांतर केले जात आहे काय?</td>
                    <td>होय</td>
                  </tr>
                  <tr>
                    <td>क) चल संपत्तीची (Fluid Resources) तरतूद पुरेशी ठेवली आहे काय?</td>
                    <td>असा व्यवहार नाही, परंतु संस्थेला बँकेचे कॅश क्रेडिट खाते आहे.</td>
                  </tr>
                </table>

                <div class="section-title">२) बाहेरील कर्जे व पत मर्यादा</div>
                <table>
                  <tr>
                    <th>अ.क्र.</th>
                    <th>पतमर्यादेचा प्रकार</th>
                    <th>कारण</th>
                    <th>मंजूर रक्कम (₹)</th>
                    <th>परतफेडीची मुदत</th>
                  </tr>
                  <tr>
                    <td class="text-center">१</td>
                    <td>बँक कॅश क्रेडिट क्लीन खाते (लातूर DCC बँक शाखा उदगीर)</td>
                    <td>सभासदांना कर्ज वाटप करण्यासाठी</td>
                    <td class="text-right">४५,००,०००.००</td>
                    <td class="text-center">१०/०६/२०२७</td>
                  </tr>
                </table>

                <div class="section-title">३) सभासदांना कर्जे व कपात</div>
                <table>
                  <tr>
                    <td style="width: 70%;">१) पोटनियमानुसार कर्ज मर्यादा पाळली जाते काय?</td>
                    <td style="width: 30%;">स.नि. कर्ज: १२ लाख | रा.अ. कर्ज: २० हजार</td>
                  </tr>
                  <tr>
                    <td>२) महाराष्ट्र सहकारी संस्था कायदा कलम ४९ अन्वये वेतनातून कपात अधिकारपत्र</td>
                    <td>होय, सर्व सभासदांचे हमीपत्र प्राप्त आहे</td>
                  </tr>
                  <tr>
                    <td>३) कर्ज व्याजदर प्रमाण</td>
                    <td>बँक व्याजदर: १०.५% | सभासद कर्ज व्याजदर: १०%</td>
                  </tr>
                </table>

                <div class="page-break"></div>

                <!-- पान ३: परिशिष्टे व कलम ८१(२)(१) विवेचन -->
                <div class="header">
                  <h2>{{ soc.name }}</h2>
                  <h3>महाराष्ट्र सहकारी संस्था नियम, १९६१ चे नियम ६९(६) अन्वये परिशिष्टे</h3>
                </div>
                <table>
                  <tr>
                    <th style="width: 15%;">परिशिष्ट क्र.</th>
                    <th style="width: 55%;">विषय / तपशील</th>
                    <th style="width: 30%;">लेखापरीक्षकाचा खुलासा</th>
                  </tr>
                  <tr>
                    <td class="text-center">परिशिष्ट क्र. १</td>
                    <td>कायदा, कानू व पोटनियम यांचे उल्लंघन झालेले व्यवहार</td>
                    <td>कृपया शेरा पहा</td>
                  </tr>
                  <tr>
                    <td class="text-center">परिशिष्ट क्र. २</td>
                    <td>हिशोबात न घेतलेल्या किंवा कमी जमा झालेल्या रकमांचा तपशील</td>
                    <td>असा व्यवहार नाही</td>
                  </tr>
                  <tr>
                    <td class="text-center">परिशिष्ट क्र. ३ व ३(अ)</td>
                    <td>अयोग्य व अनियमित दिलेल्या रकमा आणि गैरवाजवी अनधिकृत खर्च</td>
                    <td>असा व्यवहार नाही</td>
                  </tr>
                  <tr>
                    <td class="text-center">परिशिष्ट क्र. ४</td>
                    <td>संशयित व बुडीत कर्ज आणि संशयित रकमांची यादी</td>
                    <td>कृपया शेरा पहा</td>
                  </tr>
                  <tr>
                    <td class="text-center">परिशिष्ट क्र. ४(अ)</td>
                    <td>स्थावर व जंगम मालमत्ता आणि इतर जिंदगी बाबत माहिती</td>
                    <td>डेडस्टॉक शिवाय इतर मालमत्ता नाही</td>
                  </tr>
                </table>

                <div class="header" style="margin-top: 25px;">
                  <h3>महाराष्ट्र सहकारी संस्था अधिनियम, १९६० चे कलम ८१(२)(१) प्रमाणे विवेचन</h3>
                </div>
                <table>
                  <tr>
                    <th style="width: 8%;">क्र.</th>
                    <th style="width: 62%;">वैधानिक तपासणी बाबी</th>
                    <th style="width: 30%;">अभिप्राय / शेरा</th>
                  </tr>
                  <tr><td class="text-center">१</td><td>कोणतेही ऋण असल्यास त्यांच्या बऱ्याच काळ थकलेल्या रकमा</td><td>कृपया शेरा पहा</td></tr>
                  <tr><td class="text-center">२</td><td>रोख शिल्लक, कर्ज रोखे, मालमत्ता व दायित्व यांचे मूल्यांकन</td><td>कृपया शेरा पहा</td></tr>
                  <tr><td class="text-center">३</td><td>दिलेली कर्जे व उधार रकमा हितसंबंधांना बाधक आहेत काय?</td><td>नाही, सुरक्षित आहेत</td></tr>
                  <tr><td class="text-center">४</td><td>केवळ पुस्तक नोंदीद्वारे संस्था हितसंबंधांना बाधक अशी उलाढाल</td><td>नाही</td></tr>
                  <tr><td class="text-center">५</td><td>दिलेली कर्जे व उधार रकमा ठेवी म्हणून दाखविण्यात आल्या काय?</td><td>असा व्यवहार नाही</td></tr>
                  <tr><td class="text-center">६</td><td>वैयक्तिक खर्च महसूल तत्त्वावर खर्ची टाकला आहे काय?</td><td>असा व्यवहार नाही</td></tr>
                </table>

                <div class="page-break"></div>

                <!-- पान ४: तेहरीज व ताळेबंद पत्रक -->
                <div class="header">
                  <h2>{{ soc.name }}</h2>
                  <h3>दि. ३१ मार्च २०२६ अखेरचा ताळेबंद व तेहरीज पत्रक</h3>
                </div>
                <table>
                  <tr>
                    <th style="width: 50%;">देयता बाजू (Liabilities)</th>
                    <th style="width: 50%;">मालमत्ता बाजू (Assets)</th>
                  </tr>
                  <tr>
                    <td style="vertical-align: top; padding: 0;">
                      <table style="margin: 0; border: none;">
                        {% for item in liab %}
                        <tr>
                          <td style="border: none; border-bottom: 1px dotted #ccc;">{{ item['तपशील'] }}</td>
                          <td class="text-right" style="border: none; border-bottom: 1px dotted #ccc;">₹ {{ "{:,}".format(item['रक्कम']) }}</td>
                        </tr>
                        {% endfor %}
                      </table>
                    </td>
                    <td style="vertical-align: top; padding: 0;">
                      <table style="margin: 0; border: none;">
                        {% for item in assets %}
                        <tr>
                          <td style="border: none; border-bottom: 1px dotted #ccc;">{{ item['तपशील'] }}</td>
                          <td class="text-right" style="border: none; border-bottom: 1px dotted #ccc;">₹ {{ "{:,}".format(item['रक्कम']) }}</td>
                        </tr>
                        {% endfor %}
                      </table>
                    </td>
                  </tr>
                  <tr style="font-weight: bold; background-color: #eee;">
                    <td>एकूण देयता: ₹ {{ "{:,}".format(tot_liab) }}</td>
                    <td>एकूण मालमत्ता: ₹ {{ "{:,}".format(tot_assets) }}</td>
                  </tr>
                </table>

                <div class="section-title">दोष दुरुस्ती अहवाल (Audit Rectification Memo)</div>
                <table>
                  <tr>
                    <th style="width: 10%;">दोष क्र.</th>
                    <th style="width: 45%;">लेखापरीक्षणातील आक्षेप / दोष</th>
                    <th style="width: 45%;">संस्थेने केलेली दुरुस्ती / खुलासा</th>
                  </tr>
                  {% for f in faults %}
                  <tr>
                    <td class="text-center"><b>{{ f['दोष क्र.'] }}</b></td>
                    <td>{{ f['तपशील'] }}</td>
                    <td>{{ f['दुरुस्ती'] }}</td>
                  </tr>
                  {% endfor %}
                </table>

                <div class="sign-container" style="margin-top: 30px;">
                  <div class="sign-box" style="text-align: left;">
                    दिनांक: {{ soc.audit_submit_date }}<br>
                    स्थळ: {{ soc.taluka }}<br><br>
                    <strong>व्यवस्थापक / सचिव</strong><br>
                    {{ soc.name }}
                  </div>
                  <div class="sign-box" style="text-align: right;">
                    <br><br>
                    <strong>{{ soc.auditor }}</strong><br>
                    {{ soc.auditor_desig }}
                  </div>
                  <div style="clear: both;"></div>
                </div>

                </body>
                </html>
                """

                t = Template(full_html_template)
                rendered_html = t.render(
                    soc=st.session_state.society,
                    liab=st.session_state.teharij_liab.to_dict(orient='records'),
                    assets=st.session_state.teharij_assets.to_dict(orient='records'),
                    tot_liab=int(st.session_state.teharij_liab['रक्कम'].sum()),
                    tot_assets=int(st.session_state.teharij_assets['रक्कम'].sum()),
                    faults=st.session_state.audit_abc.to_dict(orient='records')
                )
                
                pdf_bytes = HTML(string=rendered_html).write_pdf()
                
                st.success("संपूर्ण वैधानिक अहवाल यशस्वीरीत्या तयार झाला!")
                st.download_button(
                    label="📥 डाऊनलोड संपूर्ण वैधानिक ऑडिट अहवाल (PDF)",
                    data=pdf_bytes,
                    file_name=f"Full_Audit_Report_{st.session_state.society['taluka']}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF तयार करताना त्रुटी आली: {str(e)}")
