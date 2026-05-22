import random
import streamlit as st

st.title("✏️ 사칙연산 계산 연습")
st.write("사칙연산 문제를 풀면서 덧셈, 뺄셈, 곱셈, 나눗셈을 재미있게 연습해 보세요!")

operations = {
    "덧셈 (+)": "+",
    "뺄셈 (−)": "-",
    "곱셈 (×)": "*",
    "나눗셈 (÷)": "/",
}

st.sidebar.header("문제 설정")
selected_ops = st.sidebar.multiselect("연습할 연산을 선택하세요", list(operations.keys()), default=list(operations.keys()))
difficulty = st.sidebar.radio("난이도", ["쉬움", "보통", "어려움"])
num_questions = st.sidebar.slider("문제 개수", min_value=5, max_value=20, value=10, step=1)

if not selected_ops:
    st.warning("하나 이상의 연산을 선택해 주세요.")
    st.stop()

if difficulty == "쉬움":
    value_range = (1, 20)
elif difficulty == "보통":
    value_range = (1, 50)
else:
    value_range = (1, 100)

st.write(f"### 선택한 연산: {', '.join(selected_ops)}")
st.write(f"### 난이도: {difficulty} / 문제 수: {num_questions}")

questions = []
answer_keys = {}

def make_question(op_symbol):
    a = random.randint(*value_range)
    b = random.randint(*value_range)
    if op_symbol == "/":
        b = random.randint(1, value_range[1])
        a = b * random.randint(1, value_range[1] // b or 1)
    if op_symbol == "-":
        a, b = max(a, b), min(a, b)
    question_text = f"{a} {op_symbol} {b} ="
    correct = eval(str(a) + op_symbol + str(b))
    if op_symbol == "/":
        correct = round(correct, 2)
        question_text = f"{a} {op_symbol} {b} = (소수 둘째 자리까지)"
    return question_text, correct

for i in range(1, num_questions + 1):
    op_key = random.choice(selected_ops)
    op_symbol = operations[op_key]
    q_text, q_answer = make_question(op_symbol)
    questions.append((i, q_text, q_answer))
    answer_keys[f"answer_{i}"] = q_answer

st.write("---")
with st.form(key="arithmetic_practice"):
    st.subheader("문제를 풀어보세요")
    user_answers = {}
    for idx, q_text, _ in questions:
        user_answers[f"answer_{idx}"] = st.text_input(f"문제 {idx}", value="", key=f"answer_input_{idx}")
    submitted = st.form_submit_button("제출하기")

if submitted:
    score = 0
    st.write("### 결과 확인")
    for idx, q_text, correct in questions:
        user_input = user_answers[f"answer_{idx}"]
        try:
            user_value = float(user_input.strip())
        except ValueError:
            user_value = None
        if user_value is not None:
            if isinstance(correct, float):
                is_right = abs(user_value - correct) < 1e-2
            else:
                is_right = user_value == correct
        else:
            is_right = False

        if is_right:
            score += 1
            st.success(f"문제 {idx}: {q_text} {user_input} ✅")
        else:
            st.error(f"문제 {idx}: {q_text} {user_input or '입력 없음'} ❌  정답: {correct}")

    st.write(f"### 총 점수: {score} / {num_questions}")
    accuracy = round(score / num_questions * 100, 1)
    st.write(f"정확도: {accuracy}%")
    if score == num_questions:
        st.balloons()
