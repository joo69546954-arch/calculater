import math
import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="다기능 계산기 + 그래프",
    page_icon="🧮",
    layout="centered"
)


def calc_basic(op, a, b):
    if op == "더하기 (+)":
        return a + b
    elif op == "빼기 (-)":
        return a - b
    elif op == "곱하기 (×)":
        return a * b
    elif op == "나누기 (÷)":
        if b == 0:
            return "오류: 0으로 나눌 수 없습니다."
        return a / b
    elif op == "모듈러 (%)":
        if b == 0:
            return "오류: 0으로 나눌 수 없습니다."
        return a % b
    elif op == "지수 (a^b)":
        try:
            return a ** b
        except OverflowError:
            return "오류: 값이 너무 큽니다."
    return "지원하지 않는 연산입니다."


def calc_log(log_type, x, base=None):
    if x <= 0:
        return "오류: 로그의 진수는 0보다 커야 합니다."

    if log_type == "자연로그 (ln x)":
        return math.log(x)
    elif log_type == "상용로그 (log10 x)":
        return math.log10(x)
    elif log_type == "밑이 b인 로그 (log_b x)":
        if base is None or base <= 0 or base == 1:
            return "오류: 밑은 0보다 크고 1이 아니어야 합니다."
        return math.log(x, base)
    return "지원하지 않는 로그 타입입니다."


def calc_trig(trig_type, angle, unit):
    if unit == "도 (degree)":
        rad = math.radians(angle)
    else:
        rad = angle

    if trig_type == "sin":
        return math.sin(rad)
    elif trig_type == "cos":
        return math.cos(rad)
    elif trig_type == "tan":
        return math.tan(rad)
    elif trig_type == "arcsin (sin⁻¹)":
        if -1 <= angle <= 1:
            return math.degrees(math.asin(angle)) if unit == "도 (degree)" else math.asin(angle)
        return "오류: arcsin 정의역은 [-1, 1]"
    elif trig_type == "arccos (cos⁻¹)":
        if -1 <= angle <= 1:
            return math.degrees(math.acos(angle)) if unit == "도 (degree)" else math.acos(angle)
        return "오류: arccos 정의역은 [-1, 1]"
    elif trig_type == "arctan (tan⁻¹)":
        return math.degrees(math.atan(angle)) if unit == "도 (degree)" else math.atan(angle)
    return "지원하지 않는 삼각함수"


def plot_polynomial(coeffs, x_min, x_max):
    """coeffs = [a_n, a_(n-1), ..., a1, a0]"""
    x = np.linspace(x_min, x_max, 400)
    y = np.polyval(coeffs, x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Polynomial'))

    fig.update_layout(
        title="다항함수 그래프",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white"
    )
    return fig


def main():
    st.title("🧮 다기능 계산기 + 다항함수 그래프")
    st.write("사칙연산, 로그, 삼각함수, 다항식 그래프를 지원합니다.")

    st.sidebar.header("연산 선택")
    mode = st.sidebar.selectbox(
        "기능을 선택하세요",
        (
            "사칙 / 모듈러 / 지수",
            "로그 연산",
            "삼각함수 연산",
            "다항함수 그래프"
        )
    )

    st.divider()

    # ---------------------- 1) 사칙연산 ----------------------
    if mode == "사칙 / 모듈러 / 지수":
        st.subheader("사칙연산 · 모듈러 · 지수")

        a = st.number_input("첫 번째 값 a", value=0.0)
        b = st.number_input("두 번째 값 b", value=0.0)

        op = st.selectbox(
            "연산 선택",
            [
                "더하기 (+)",
                "빼기 (-)",
                "곱하기 (×)",
                "나누기 (÷)",
                "모듈러 (%)",
                "지수 (a^b)"
            ]
        )

        if st.button("계산하기"):
            st.success(f"결과: {calc_basic(op, a, b)}")

    # ---------------------- 2) 로그 연산 ----------------------
    elif mode == "로그 연산":
        st.subheader("로그 연산")

        x = st.number_input("진수 x", value=1.0)
        log_type = st.selectbox(
            "로그 종류",
            ["자연로그 (ln x)", "상용로그 (log10 x)", "밑이 b인 로그 (log_b x)"]
        )

        base = None
        if log_type == "밑이 b인 로그 (log_b x)":
            base = st.number_input("밑 b", value=2.0)

        if st.button("로그 계산하기"):
            st.success(f"결과: {calc_log(log_type, x, base)}")

    # ---------------------- 3) 삼각함수 ----------------------
    elif mode == "삼각함수 연산":
        st.subheader("삼각함수 연산")

        trig_type = st.selectbox(
            "삼각함수",
            ["sin", "cos", "tan", "arcsin (sin⁻¹)", "arccos (cos⁻¹)", "arctan (tan⁻¹)"]
        )

        unit = st.radio("각도 단위", ["도 (degree)", "라디안 (radian)"], horizontal=True)

        angle = st.number_input("입력값", value=0.0)

        if st.button("삼각함수 계산하기"):
            st.success(f"결과: {calc_trig(trig_type, angle, unit)}")

    # ---------------------- 4) 다항함수 그래프 ----------------------
    elif mode == "다항함수 그래프":
        st.subheader("다항함수 그래프 그리기 (Plotly)")

        st.write("계수를 높은 차수부터 입력하세요. 예: 2x³ + 0x² + 3x + 1 → **2, 0, 3, 1**")

        coeff_input = st.text_input("계수 입력 (쉼표로 구분)", "1, -3, 2")
        x_min = st.number_input("x 최소값", value=-10.0)
        x_max = st.number_input("x 최대값", value=10.0)

        if st.button("그래프 그리기"):
            try:
                coeffs = [float(c.strip()) for c in coeff_input.split(",")]
                fig = plot_polynomial(coeffs, x_min, x_max)
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.error("계수 입력 형식을 확인하세요. 예: 1, -3, 2")



if __name__ == "__main__":
    main()
