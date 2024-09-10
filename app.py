from openai import OpenAI
import streamlit as st

# OpenAI API 클라이언트 생성
#client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
client = OpenAI(
  api_key=st.secrets["api_key"],
) 

# 조사할 항목 리스트
TOPICS = {
    "대륙": "Which continent does it involed",
    "수도": "Capital",
    "화폐": "Currency",
    "언어": "Language",
    "음식": "Famous foods",
    "랜드마크": "Landmark",
    "종교": "Religion",
    "유명한 사람": "famous person"
}

# 이모지 사전
EMOJIS = {
    "대륙": "🌍",
    "수도": "🏙️",
    "화폐": "💰",
    "언어": "🗣️",
    "음식": "🍽️",
    "랜드마크": "🏛️",
    "종교": "⛪",
    "유명한 사람": "🤴"
}

def get_country_info_from_openai(country_name, topic):
    """OpenAI API를 통해 나라 정보 생성"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"너는 한국의 초등학교 5학년 영어선생님이야. 만약에 {country_name}을 Korean으로 입력하면 절대로 대답해주지 마. 꼭 알파벳으로 입력했을 때만 대답해 줘. 왜냐면 이건 영어 수업이니까."},
            {"role": "user", "content": f'''
             Tell me one or two sentence what is {topic} of {country_name}, and about the {topic} of {country_name} in Korean for elementary school students, and give one or two name of {topic} about {topic} of {country_name} in English right after Korean explanation. And do not print {topic}. 
             예시: 
             유명한 사람
             유키 구라모토는 일본의 유명한 작곡가입니다.(Kuramoto Yuki)...'''}
        ]
    )
    return completion.choices[0].message.content

# 앱 제목
st.title("나라에 대해 알아보기 🌍")

st.divider()  # Streamlit version 1.23+
st.header("사용방법")
st.markdown("### 1️⃣ 알고 싶은 나라 이름을 영어로 적고 엔터키 또는 나라 알아보기 버튼을 눌러주세요.")
st.markdown("### 2️⃣ 더 알고 싶은 나라가 있으면 나라 이름을 다시 적고 엔터나 버튼을 눌러주세요.")
st.markdown("### ❗ 이 앱은 완벽하지 않아요. 실수할 때가 있으면 나라 알아보기 버튼을 다시 눌러주세요.")



# 나라 이름 입력
country_name = st.text_input("나라 이름을 영어로 입력하세요:")

# "다른 나라 알아보기" 버튼 - 세션 상태 초기화
if st.button("나라 알아보기"):
    st.session_state["country_name"] = ""  # 나라 이름 초기화

# 세션 상태에서 나라 이름이 없다면 입력 필드를 초기화
if "country_name" not in st.session_state:
    st.session_state["country_name"] = ""

if country_name:
    st.write(f"### {country_name}에 대해 알아볼까요?")

    # 각 항목에 대해 OpenAI API로 정보 가져오기
    for topic_kor, topic_eng in TOPICS.items():
        st.write(f"#### {EMOJIS[topic_kor]} **{topic_kor}**")
        result = get_country_info_from_openai(country_name, topic_eng)
        st.write(result)

# 예쁜 UI를 위해 배경 및 글꼴 스타일 설정
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;  /* 하늘색 배경 */
        color: #000000;  /* 검은색 텍스트 */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;  /* 제목에 약간 어두운 색을 적용 */
    }
    </style>
    """, 
    unsafe_allow_html=True
)
