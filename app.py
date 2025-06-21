# app.py 

import streamlit as st
from gpt_processor import gpt_structure_text
from proof_checker import check_full_proof
import os

if os.getenv("OPENAI_API_KEY") is None:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다.", icon="🔑")
    st.stop()

st.set_page_config(layout="centered", page_title="선형대수 증명 논리 검증 시스템")
st.title("👨‍🏫 자연어 기반 선형대수 증명 논리 검증 시스템")
st.markdown("증명의 각 단계를 **줄바꿈 Enter**으로 구분하고, **사용한 정리는 `'정리_이름'` 형식**으로 명시해주세요.")
st.header("증명 입력 ✍️")
user_proof_input = st.text_area(
    "여기에 증명을 한 줄에 한 단계씩 입력해주세요:",
    "V는 벡터 공간이다.\n'유일한_덧셈_항등원' 정리에 의해, V의 덧셈 항등원은 유일하다.",
    height=200
)

if st.button("🚀 논리 검증 시작!"):
    if not user_proof_input.strip():
        st.error("증명 내용을 입력해주세요.", icon="❗")
    else:
        st.header("최종 검증 결과 🔬")

        structured_proof, error_message = gpt_structure_text(user_proof_input)

        if error_message:
            st.error(f"오류 발생: {error_message}", icon="🔥")
        elif structured_proof:
            
            with st.spinner("🤔 논리적 타당성을 검증하고 있습니다..."):
                validation_results = check_full_proof(structured_proof)

            for res in validation_results:
                if "결함 없음" in res:
                    st.success(res, icon="✅")
                elif "논리적 결함" in res or "검증이 불가능" in res:
                    st.error(res, icon="🚨")
                else:
                    st.info(res, icon="ℹ️")

st.markdown("---")
st.info("💡 **참고:** 이 시스템은 학습 보조 도구이며, 복잡한 수학적 추론을 완벽하게 대체하지는 않습니다.")