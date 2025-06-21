# gpt_processor.py

import os, openai, json

try: client = openai.OpenAI()
except: client = None

def gpt_structure_text(user_proof: str):
    if not client: return None, "OpenAI 클라이언트 초기화 실패"

    system_prompt = """
    You are a machine that extracts the main conclusion from a single sentence of a mathematical proof.
    For the user's input sentence, respond with ONLY a single JSON object with one key, "결론".
    The value should be the main conclusive statement of the sentence.
    Example:
    User: "따라서 '벡터_덧셈_교환법칙'에 의해, u+v = v+u 이다."
    Assistant: {"결론": "u+v = v+u"}
    """
    
    steps_text = [s.strip() for s in user_proof.strip().split('\n') if s.strip()]
    structured_proof = []
    error_log = []

    for i, step_text in enumerate(steps_text):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": step_text}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            response_content = response.choices[0].message.content
            if response_content is None: raise ValueError("API가 빈 응답 반환")
            
            step_data = json.loads(response_content)
            
            full_step_data = {
                "단계": i + 1,
                "내용": step_text,
                "결론": step_data.get("결론", "")
            }
            structured_proof.append(full_step_data)

        except Exception as e:
            error_log.append(f"Step {i+1} 처리 중 오류: {e}")

    if error_log:
        return None, ". ".join(error_log)
    
    return structured_proof, None