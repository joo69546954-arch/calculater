import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# -------------------------------------------------------------
#   Streamlit 기본 설정
# -------------------------------------------------------------
st.set_page_config(
    page_title="계산기 + 세계인구 분석",
    page_icon="🌍",
    layout="wide"
)

st.sidebar.title("📌 메뉴 선택")
app_mode = st.sidebar.selectbox(
    "기능을 선택하세요",
    ["계산기", "연도별 세계인구 분석"]
)

# -------------------------------------------------------------
#   계산기 함수들
# -------------------------------------------------------------
def calc_basic(op, a, b):
    if op == "더하기 (+)": return a + b
    if op == "빼기 (-)": return a - b
    if op == "곱하기 (×)": return a * b
    if op == "나누기 (÷)":
        return "0으로 나눌 수 없습니다." if b == 0 else a / b
    if op == "모듈러 (%)":
        return "0으로 나눌 수 없습니다." if b == 0 else a % b
    if op == "지수 (a^b)":
        try: return a ** b
        except: return "오류: 값이 너무 큽니다."
    return "지원하지 않는 연산입니다."


def calc_log(log_type, x, base=None):
    if x <= 0:
        return "로그의 진수는 0보다 커야 합니다."
    if log_type == "자연로그 (ln x)": return math.log(x)
    if log_type == "상용로그 (log10 x)": return math.log10(x)
    if log_type == "밑이 b인 로그 (log_b x)":
        if base in [None, 1] or base <= 0:
            return "밑은 양수이고 1이 아니어야 합니다."
        return math.log(x, base)
    return "지원하지 않는 로그 타입입니다."


def calc_trig(trig_type, angle, unit):
    if trig_type in ["sin", "cos", "tan"]:
        rad = math.radians(angle) if unit == "도 (degree)" else angle
        return {"sin": math.sin(rad), "cos": math.cos(rad), "tan": math.tan(rad)}[trig_type]

    # 역삼각함수
    if abs(angle) > 1 and trig_type != "arctan (tan⁻¹)":
        return "정의역 오류: 입력값은 -1 ~ 1이어야 합니다."
    if trig_type == "arcsin (sin⁻¹)": val = math.asin(angle)
    elif trig_type == "arccos (cos⁻¹)": val = math.acos(angle)
    else: val = math.atan(angle)

    return math.degrees(val) if unit == "도 (degree)" else val


def plot_polynomial(coeffs, x_min, x_max):
    x = np.linspace(x_min, x_max, 400)
    y = np.polyval(coeffs, x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines"))
    fig.update_layout(
        title="다항함수 그래프",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------
#   계산기 화면 출력
# -------------------------------------------------------------
def calculator_app():
    st.title("🧮 다기능 계산기")

    mode = st.sidebar.radio(
        "계산 기능 선택",
        ["사칙 / 모듈러 / 지수", "로그 연산", "삼각함수 연산", "다항함수 그래프"]
    )

    st.divider()

    if mode == "사칙 / 모듈러 / 지수":
        st.subheader("사칙 / 모듈러 / 지수 계산")
        a = st.number_input("a 값", value=0.0)
        b = st.number_input("b 값", value=0.0)
        op = st.selectbox("연산", ["더하기 (+)", "빼기 (-)", "곱하기 (×)", "나누기 (÷)", "모듈러 (%)", "지수 (a^b)"])
        if st.button("계산하기"):
            st.success(calc_basic(op, a, b))

    elif mode == "로그 연산":
        st.subheader("로그 계산")
        x = st.number_input("진수 x", value=1.0, min_value=0.0)
        log_type = st.selectbox("로그 종류", ["자연로그 (ln x)", "상용로그 (log10 x)", "밑이 b인 로그 (log_b x)"])
        base = st.number_input("밑 b", value=2.0) if log_type == "밑이 b인 로그 (log_b x)" else None
        if st.button("계산하기"):
            st.success(calc_log(log_type, x, base))

    elif mode == "삼각함수 연산":
        st.subheader("삼각함수 계산")
        trig = st.selectbox("함수 선택", ["sin", "cos", "tan", "arcsin (sin⁻¹)", "arccos (cos⁻¹)", "arctan (tan⁻¹)"])
        unit = st.radio("각도 단위", ["도 (degree)", "라디안 (radian)"], horizontal=True)
        angle = st.number_input("입력값", value=0.0)
        if st.button("계산하기"):
            st.success(calc_trig(trig, angle, unit))

    else:  # 다항함수
        st.subheader("다항함수 그래프 그리기")
        coeff_input = st.text_input("계수 입력 (예: 2, -1, 3)", "1, -3, 2")
        x_min = st.number_input("x 최소", value=-10.0)
        x_max = st.number_input("x 최대", value=10.0)
        if st.button("그래프 그리기"):
            coeffs = [float(c.strip()) for c in coeff_input.split(",")]
            fig = plot_polynomial(coeffs, x_min, x_max)
            st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
#   연도별 세계인구 분석 모듈
# -------------------------------------------------------------

YEARS = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022]

@st.cache_data
def load_population_data(upload_file):
    if upload_file is not None:
        return pd.read_csv(upload_file)
    try:
        return pd.read_csv("world_population.csv")
    except:
        return None


def population_app():
    st.title("🌍 연도별 세계인구 분석")

    upload = st.file_uploader("world_population.csv 업로드 (선택)", type=["csv"])
    df = load_population_data(upload)

    if df is None:
        st.error("⚠ world_population.csv 파일이 필요합니다.")
        return

    year = st.selectbox("연도 선택", YEARS)
    pop_col = f"{year} Population"

    if pop_col not in df.columns:
        st.error(f"⚠ 데이터에 '{pop_col}' 컬럼이 없습니다.")
        return

    data = df[["Country/Territory", "CCA3", pop_col]].copy()
    data.rename(columns={pop_col: "Population"}, inplace=True)

    total_pop = data["Population"].sum()

    # -------------------------------
    # 1) 절대 인구수 구간 색칠 지도
    # -------------------------------
    st.subheader("① 절대 인구수 기반 세계지도")

    bins = [0, 1_000_000, 10_000_000, 50_000_000, 100_000_000, 500_000_000, 2_000_000_000]
    labels = ["<1M", "1M–10M", "10M–50M", "50M–100M", "100M–500M", ">500M"]

    data["pop_range"] = pd.cut(data["Population"], bins=bins, labels=labels)

    fig1 = px.choropleth(
        data,
        locations="CCA3",
        color="pop_range",
        hover_name="Country/Territory",
        labels={"pop_range": "Population Range"},
        template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # -------------------------------
    # 2) 세계 인구 비율 구간 지도
    # -------------------------------
    st.subheader("② 세계 인구 대비 비율 기반 세계지도")

    data["share"] = data["Population"] / total_pop * 100
    share_bins = [0, 0.05, 0.1, 0.5, 1, 5, 100]
    share_labels = ["<0.05%", "0.05–0.1%", "0.1–0.5%", "0.5–1%", "1–5%", ">5%"]

    data["share_range"] = pd.cut(data["share"], bins=share_bins, labels=share_labels)

    fig2 = px.choropleth(
        data,
        locations="CCA3",
        color="share_range",
        hover_name="Country/Territory",
        hover_data={"share": ":.2f"},
        labels={"share_range": "World Share (%)"},
        template="plotly_white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------
#   메인 실행
# -------------------------------------------------------------
if app_mode == "계산기":
    calculator_app()
else:
    population_app()
