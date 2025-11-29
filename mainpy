import math
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="다기능 계산기",
    page_icon="🧮",
    layout="centered"
)


def calc_basic(op, a, b):
    """사칙연산 및 모듈러, 지수 연산"""
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
    else:
        return "지원하지 않는 연산입니다."


def calc_log(log_type, x, base=None):
    """로그 연산"""
    if x <= 0:
        return "오류: 로그의 밑은 양수여야 하고, 진수는 0보다 커야 합니다."

    if log_type == "자연로그 (ln x)":
        return math.log(x)
    elif log_type == "상용로그 (log10 x)":
        return math.log10(x)
    elif log_type == "밑이 b인 로그 (log_b x)":
        if base is None or base <= 0 or base == 1:
            return "오류: 밑은 0보다 크고 1이 아니어야 합니다."
        return math.log(x, base)
    else:
        return "지원하지 않는 로그 타입입니다."


def calc_trig(trig_type, angle, unit):
    """삼각함수 연산"""
    # 각도 단위를 라디안으로 변환
    if unit == "도 (degree)":
        rad = math.radians(angle)
    else:
        rad = angle

    if trig_type == "sin":
        return math.sin(rad)
    elif trig_type == "cos":
        return math.cos(rad)
    elif trig_type == "tan":
        try:
            return math.tan(rad)
        except OverflowError:
            return "오류: tan 값이 정의되지 않습니다."
    elif trig_type == "arcsin (sin⁻¹)":
        if -1 <= angle <= 1:
            return math.degrees(math.asin(angle)) if unit == "도 (degree)" else math.asin(angle)
        return "오류: arcsin 정의역은 [-1, 1] 입니다."
    elif trig_type == "arccos (cos⁻¹)":
        if -1 <= angle <= 1:
            return math.degrees(math.acos(angle)) if unit == "도 (degree)" else math.acos(angle)
        return "오류: arccos 정의역은 [-1, 1] 입니다."
    elif trig_type == "arctan (tan⁻¹)":
        # arctan은 모든 실수에 대해 정의
        return math.degrees(math.atan(angle)) if unit == "도 (degree)" else math.atan(angle)
    else:
        return "지원하지 않는 삼각함수입니다."


def main():
    st.title("🧮 다기능 계산기 웹앱")
    st.write(
        """
        깃허브 + Streamlit으로 만드는 간단한 계산기 예제입니다.  
        **사칙연산, 모듈러, 지수, 로그, 삼각함수** 연산을 지원합니다.
        """
    )

    # 사이드바: 연산 종류 선택
    st.sidebar.header("연산 설정")
    mode = st.sidebar.selectbox(
        "연산 종류를 선택하세요",
        (
            "사칙 / 모듈러 / 지수",
            "로그 연산",
            "삼각함수 연산"
        )
    )

    st.divider()

    # 1) 사칙 / 모듈러 / 지수
    if mode == "사칙 / 모듈러 / 지수":
        st.subheader("사칙연산 · 모듈러 · 지수 연산")

        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("첫 번째 숫자 (a)", value=0.0, format="%.8f")
        with col2:
            b = st.number_input("두 번째 숫자 (b)", value=0.0, format="%.8f")

        op = st.selectbox(
            "연산을 선택하세요",
            (
                "더하기 (+)",
                "빼기 (-)",
                "곱하기 (×)",
                "나누기 (÷)",
                "모듈러 (%)",
                "지수 (a^b)"
            )
        )

        if st.button("계산하기"):
            result = calc_basic(op, a, b)
            st.success(f"결과: {result}")

    # 2) 로그 연산
    elif mode == "로그 연산":
        st.subheader("로그 연산")

        x = st.number_input("진수 x (x > 0)", value=1.0, min_value=0.0, format="%.8f")

        log_type = st.selectbox(
            "로그 타입 선택",
            (
                "자연로그 (ln x)",
                "상용로그 (log10 x)",
                "밑이 b인 로그 (log_b x)"
            )
        )

        base = None
        if log_type == "밑이 b인 로그 (log_b x)":
            base = st.number_input("밑 b (b > 0, b ≠ 1)", value=2.0, format="%.8f")

        if st.button("로그 계산하기"):
            result = calc_log(log_type, x, base)
            st.success(f"결과: {result}")

    # 3) 삼각함수 연산
    elif mode == "삼각함수 연산":
        st.subheader("삼각함수 연산")

        trig_type = st.selectbox(
            "삼각함수 종류 선택",
            (
                "sin",
                "cos",
                "tan",
                "arcsin (sin⁻¹)",
                "arccos (cos⁻¹)",
                "arctan (tan⁻¹)"
            )
        )

        st.caption(
            """
            - sin, cos, tan 선택 시 → 입력 값은 **각도**  
            - arcsin, arccos, arctan 선택 시 → 입력 값은 **값** (예: sin 값)
            """
        )

        unit = st.radio(
            "각도 단위 선택 (출력/입력 해석에 사용)",
            ("도 (degree)", "라디안 (radian)"),
            horizontal=True
        )

        if trig_type in ["sin", "cos", "tan"]:
            angle = st.number_input(
                "각도를 입력하세요",
                value=0.0,
                format="%.8f"
            )
            value_for_calc = angle
        else:
            # 역삼각함수 입력값
            value_for_calc = st.number_input(
                "함수값을 입력하세요 (예: sin 값)",
                value=0.0,
                format="%.8f"
            )

        if st.button("삼각함수 계산하기"):
            result = calc_trig(trig_type, value_for_calc, unit)
            st.success(f"결과: {result}")


if __name__ == "__main__":
    main()
