import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 이용해 영화의 관객 변화를 그래프로 살펴봅니다.")

# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.info("데이터 주소나 CSV 파일의 열 이름을 확인해 주세요.")
    st.stop()


# ============================================================
# 데이터 기본 확인
# ============================================================

st.divider()

st.header("1. 시간에 따른 영화 관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화가 기록된 날짜별 일관객 수의 변화를 확인할 수 있습니다."
)


# ============================================================
# 영화 선택
# ============================================================

movie_list = sorted(
    df["영화명"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_movie = st.selectbox(
    "🎞️ 영화를 선택하세요",
    movie_list
)


# ============================================================
# 첫 번째 그래프
# ============================================================

movie_df = df[df["영화명"] == selected_movie].copy()

movie_df = movie_df.sort_values("날짜")


fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,.0f}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 그래프 설명 입력 자리
# ============================================================

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 적어 보세요.",
    placeholder="예: 개봉 직후 관객 수가 가장 많고 시간이 지나면서 관객 수가 감소하는 것을 알 수 있다.",
    height=100,
    key="graph1_note"
)


# ============================================================
# 다음 그래프를 추가할 공간
# ============================================================

st.divider()

st.header("2. 다음 그래프")

st.info(
    "앞으로 새로운 그래프를 추가할 때 이 구역 아래에 그래프와 "
    "'이 그래프로 알 수 있는 것' 부분을 추가하면 됩니다."
)

# ============================================================
# 추가 그래프 작성 예시 공간
# ============================================================

# 새로운 그래프를 추가할 때 아래와 같은 형식으로 작성하면 됩니다.
#
# st.subheader("그래프 제목")
#
# fig2 = px.bar(...)
# st.plotly_chart(fig2, use_container_width=True)
#
# st.subheader("📝 이 그래프로 알 수 있는 것")
# st.text_area(
#     "그래프에서 발견한 특징을 적어 보세요.",
#     key="graph2_note"
# )
#
# st.divider()
#
# st.header("3. 다음 그래프")
#
# 이렇게 그래프 구역을 계속 추가할 수 있습니다.


# ============================================================
# 데이터 정보
# ============================================================

st.divider()

st.header("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 기록 수", f"{len(df):,}개")

with col2:
    st.metric("기록된 영화 수", f"{df['영화명'].nunique():,}편")

with col3:
    st.metric(
        "데이터 기간",
        f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
        f"{df['날짜'].max().strftime('%Y-%m-%d')}"
    )
