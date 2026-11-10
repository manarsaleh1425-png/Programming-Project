import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import requests

st.set_page_config(page_title="SPACE MISSION", page_icon="🚀", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"
if "points" not in st.session_state:
    st.session_state.points = 0
if "quiz_done" not in st.session_state:
    st.session_state.quiz_done = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
}
.stApp {
    background:
    radial-gradient(circle at 15% 20%, #192b59 0%, transparent 30%),
    radial-gradient(circle at 85% 70%, #30164d 0%, transparent 30%),
    #050b19;
    color: white;
}
header, footer {visibility: hidden;}
.hero {
    text-align: center;
    padding: 45px 15px;
    border: 1px solid #28446e;
    border-radius: 25px;
    background: linear-gradient(135deg, #101e3b, #11132c);
}
.hero h1 {color: #8de3ff; font-size: 48px; font-weight: 900;}
.hero p {color: #c6d7f5; font-size: 18px;}
.card {
    background: #111d35;
    border: 1px solid #31558a;
    border-radius: 18px;
    padding: 15px;
    text-align: center;
}
h1, h2, h3 {color: #8de3ff;}
.stButton > button {
    background: linear-gradient(90deg, #1769aa, #7446b8);
    color: white;
    border: 1px solid #75cfff;
    border-radius: 12px;
    min-height: 48px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


def go_home():
    st.session_state.page = "home"


def page_title(title, description):
    st.markdown(
        f"<h1 style='text-align:center'>{title}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='text-align:center;color:#c6d7f5'>{description}</p>",
        unsafe_allow_html=True
    )
    st.button("⬅️ العودة إلى الواجهة الرئيسية", on_click=go_home)
    st.divider()


# الصفحة الرئيسية
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div style="font-size:60px">🚀</div>
        <h1>SPACE MISSION</h1>
        <p>مهمتك تبدأ من هنا ... اكتشف الكون، واستكشف الكواكب!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<h2 style='text-align:center'>🌌 مركز قيادة المستكشفين</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align:center;color:white'>اختر وجهتك</h3>",
        unsafe_allow_html=True
    )

    sections = [
        ("🪐", "استكشاف الكواكب", "planets"),
        ("🚀", "الرحلات الفضائية", "journeys"),
        ("🌞", "محاكاة المدارات", "orbits"),
        ("💻", "مختبر البرمجة الرياضية", "lab"),
        ("🏆", "المهام والتحديات", "challenges")
    ]

    cols = st.columns(3)
    for i, (emoji, title, key) in enumerate(sections):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
                <div style="font-size:40px">{emoji}</div>
                <h3>{title}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button("افتح القسم", key=f"open_{key}"):
                st.session_state.page = key
                st.rerun()

    st.markdown(
        f"<h3 style='text-align:center'>🏅 نقاط المستكشف: {st.session_state.points}</h3>",
        unsafe_allow_html=True
    )


# استكشاف الكواكب
elif st.session_state.page == "planets":
    page_title("🪐 استكشاف الكواكب", "تعرفي على كواكب المجموعة الشمسية")

    planets = {
        "عطارد": ("أقرب الكواكب إلى الشمس، ويتميز بصغر حجمه.", "Mercury"),
        "الزهرة": ("ثاني كواكب المجموعة الشمسية، وله غلاف جوي كثيف.", "Venus"),
        "الأرض": ("كوكبنا، ويتميز بوجود الماء والحياة.", "Earth"),
        "المريخ": ("يعرف بالكوكب الأحمر بسبب لون سطحه.", "Mars"),
        "المشتري": ("أكبر كواكب المجموعة الشمسية.", "Jupiter"),
        "زحل": ("يشتهر بحلقاته الجميلة.", "Saturn"),
        "أورانوس": ("كوكب عملاق جليدي ويميل محوره بشكل كبير.", "Uranus"),
        "نبتون": ("أبعد كواكب المجموعة الشمسية عن الشمس.", "Neptune")
    }

    selected = st.selectbox("اختاري كوكبًا:", list(planets.keys()))
    description, english_name = planets[selected]

    st.markdown(f"## 🪐 {selected}")
    st.info(description)

    with st.spinner("جاري تحميل صورة الكوكب..."):
        try:
            response = requests.get(
                "https://images-api.nasa.gov/search",
                params={"q": english_name, "media_type": "image"},
                timeout=15
            )
            response.raise_for_status()
            items = response.json()["collection"]["items"]
            image_url = None

            for item in items:
                data = item.get("data", [{}])[0]
                links = item.get("links", [])
                if english_name.lower() in data.get("title", "").lower() and links:
                    image_url = links[0].get("href")
                    break

            if not image_url and items:
                links = items[0].get("links", [])
                if links:
                    image_url = links[0].get("href")

            if image_url:
                st.image(image_url, caption=f"{selected} - NASA",
                         use_container_width=True)
            else:
                st.warning("لم يتم العثور على صورة متاحة حاليًا.")
        except Exception:
            st.warning("تعذر تحميل الصورة. تحققي من اتصال الإنترنت.")

    st.caption("مصدر الصور: NASA Image and Video Library")


# الرحلات الفضائية
elif st.session_state.page == "journeys":
    page_title("🚀 الرحلات الفضائية", "اختاري وجهة رحلتك الافتراضية")

    planet_names = [
        "عطارد", "الزهرة", "الأرض", "المريخ",
        "المشتري", "زحل", "أورانوس", "نبتون"
    ]
    distances = {
        "عطارد": 0.39, "الزهرة": 0.72, "الأرض": 1.00,
        "المريخ": 1.52, "المشتري": 5.20, "زحل": 9.58,
        "أورانوس": 19.2, "نبتون": 30.05
    }

    destination = st.selectbox("إلى أي كوكب تريدين الذهاب؟", planet_names)

    if st.button("🚀 انطلق في الرحلة"):
        st.success(f"تم تحديد وجهتك: كوكب {destination}")
        st.info(
            f"متوسط بُعد {destination} عن الشمس هو "
            f"{distances[destination]} وحدة فلكية."
        )

        st.components.v1.html("""
        <button onclick="playLaunch()"
        style="background:#1769aa;color:white;padding:12px;
        border:0;border-radius:12px;font-size:16px;">
        🔊 تشغيل صوت الإطلاق
        </button>
        <script>
        function playLaunch() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(100, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(600, ctx.currentTime + 1);
            gain.gain.setValueAtTime(0.15, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.5);
            osc.start();
            osc.stop(ctx.currentTime + 1.5);
        }
        </script>
        """, height=65)

        st.caption("هذه رحلة تعليمية افتراضية وليست مسارًا حقيقيًا.")


# محاكاة المدارات
elif st.session_state.page == "orbits":
    page_title("🌞 محاكاة المدارات", "شاهدي نموذجًا مبسطًا لحركة الكواكب حول الشمس")

    angle = st.slider("غيّري زاوية حركة الكواكب:", 0, 360, 45)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_facecolor("#071126")
    fig.patch.set_facecolor("#071126")
    ax.scatter(0, 0, color="yellow", s=350, label="الشمس")

    orbit_data = [
        ("عطارد", 1.0, "#aaaaaa"),
        ("الزهرة", 1.5, "#e5b56b"),
        ("الأرض", 2.1, "#42a5f5"),
        ("المريخ", 2.7, "#e57373")
    ]

    theta = np.linspace(0, 2 * np.pi, 300)

    for name, radius, color in orbit_data:
        ax.plot(radius * np.cos(theta), radius * np.sin(theta),
                color=color, alpha=0.5)
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        ax.scatter(x, y, color=color, s=90, label=name)

    ax.set_aspect("equal")
    ax.legend(facecolor="#15233d", labelcolor="white")
    ax.set_title("نموذج المدارات حول الشمس", color="white")
    ax.tick_params(colors="white")
    st.pyplot(fig)
    st.info("غيّري زاوية الحركة ولاحظي تغير مواقع الكواكب في النموذج.")


# مختبر البرمجة الرياضية
elif st.session_state.page == "lab":
    page_title(
        "💻 مختبر البرمجة الرياضية",
        "تحكمي بمركبة افتراضية باستخدام مفاهيم Python"
    )

    speed = st.slider("سرعة المركبة الافتراضية:", 1, 20, 5)
    direction = st.slider("زاوية الاتجاه:", 0, 360, 45)
    time = st.slider("زمن المحاكاة:", 1, 10, 3)

    if st.button("احسب حركة المركبة"):
        radians = math.radians(direction)
        x = speed * math.cos(radians) * time
        y = speed * math.sin(radians) * time
        distance = math.sqrt(x**2 + y**2)

        st.success("تم تنفيذ المحاكاة الافتراضية!")

        c1, c2, c3 = st.columns(3)
        c1.metric("الموقع الأفقي", f"{x:.2f}")
        c2.metric("الموقع الرأسي", f"{y:.2f}")
        c3.metric("المسافة", f"{distance:.2f}")

        st.write("رسم مسار المركبة:")
        fig, ax = plt.subplots()
        ax.plot([0, x], [0, y], marker="o")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("المسار الافتراضي للمركبة")
        ax.grid(True)
        st.pyplot(fig)

        st.caption(
            "استخدمنا الدوال المثلثية والجذر التربيعي من مكتبة math."
        )


# المهام والتحديات
elif st.session_state.page == "challenges":
    page_title("🏆 المهام والتحديات", "اختبري معلوماتك الفضائية")

    st.write("**السؤال الأول: ما أكبر كواكب المجموعة الشمسية؟**")

    answer = st.radio(
        "اختاري الإجابة:",
        ["الأرض", "المشتري", "المريخ", "عطارد"],
        key="quiz_answer"
    )

    if st.button("تحققي من الإجابة"):
        if answer == "المشتري":
            st.success("إجابة صحيحة! أحسنتِ 👏")
            if not st.session_state.quiz_done:
                st.session_state.points += 10
                st.session_state.quiz_done = True
        else:
            st.error("حاولي مرة أخرى!")

    st.write(f"🏅 مجموع نقاطك: {st.session_state.points}")
