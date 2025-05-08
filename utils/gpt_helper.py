# utils/gpt_helper.py

import os
from openai import OpenAI  # ✅ 최신 버전 방식

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),  # ✅ 반드시 필요!
    base_url="https://api.openai.com/v1"     # ✅ 명시적으로 설정
)


COIN_PROMPT_TEMPLATE = """
아래 문장에서 언급된 암호화폐 이름을 영어로 하나만 추출해줘.
yfinance에서 사용하는 형식으로 반환해줘 (예: bitcoin → BTC-USD).
문장: "{user_input}"
못 찾겠으면 "None"이라고만 답해줘.
"""

def extract_coin_name(user_input: str) -> str:
    prompt = COIN_PROMPT_TEMPLATE.format(user_input=user_input)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# ✅ 뉴스/트윗 요약용 함수도 같이 정의
SUMMARIZE_PROMPT_TEMPLATE = """
다음은 {label} 데이터입니다. 초보자도 이해할 수 있도록 간결하게 요약해줘:\n\n{text}
"""

def summarize_content(text_list, label="뉴스"):
    content = "\n\n".join(text_list[:5])
    prompt = SUMMARIZE_PROMPT_TEMPLATE.format(label=label, text=content)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# 테스트용
if __name__ == "__main__":
    print(extract_coin_name("비트코인 시세 어때?"))
