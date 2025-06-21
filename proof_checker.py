# proof_checker.py 

from theorems import theorem_dict
import re

def is_premise_met(current_step_info, previous_steps_info):
    step_content = current_step_info.get("내용", "")
    
    match = re.search(r'[\'"](.+?)[\'"]', step_content)
    used_theorem = match.group(1) if match else None

    if not used_theorem or used_theorem not in theorem_dict:
        return True, "이 단계는 시작 전제이거나, 특정 정리를 사용하지 않았습니다."

    required_premises = theorem_dict[used_theorem]["가정"]
    if not required_premises:
        return True, f"'{used_theorem}' 사용. (별도 전제 필요 없음)"

    known_facts = set()
    all_previous_contents = ""
    for step in previous_steps_info:
        conclusion_text = step.get("결론", "")
        if conclusion_text: known_facts.add(conclusion_text.strip())
        all_previous_contents += " " + step.get("내용", "")

    missing_premises = []
    for required_premise in required_premises:
        premise_satisfied = False
        if any(required_premise.lower() in fact.lower() for fact in known_facts):
            premise_satisfied = True
        elif required_premise.lower() in all_previous_contents.lower():
            premise_satisfied = True
        if not premise_satisfied:
            missing_premises.append(required_premise)

    if not missing_premises:
        return True, f"'{used_theorem}' 사용. 모든 전제 충족."
    else:
        return False, f"'{used_theorem}' 사용. 다음 전제가 충족되지 않아 논리적 결함 있음: {', '.join(missing_premises)}"

def check_full_proof(structured_proof_steps):
    if not structured_proof_steps: return ["증명 내용이 없습니다."]

    results = []
    previous_steps_info = []
    flaw_found = False

    for i, current_step in enumerate(structured_proof_steps):
        step_num = current_step.get('단계', i + 1)
        is_valid, message = is_premise_met(current_step, previous_steps_info)
        results.append(f"Step {step_num}: {message}")
        if not is_valid:
            flaw_found = True
            results.append("논리적 결함 발견! 검증 중단.")
            break
        previous_steps_info.append(current_step)

    if not flaw_found:
        results.append("모든 단계에서 논리적 결함 없음!")
    return results