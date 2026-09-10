import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

except Exception:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.info("데이터 주소나 CSV 파일의 열 이름을 확인해 주세요.")
    st.stop()


# ============================================================
# 1. 영화별 날짜에 따른 일관객 변화
# ============================================================

st.divider()

st.header("1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화가 기록된 날짜별 일관객 수의 변화를 확인할 수 있습니다."
)


# ------------------------------------------------------------
# 영화 선택
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 첫 번째 그래프
# ------------------------------------------------------------

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,.0f}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=550
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ------------------------------------------------------------
# 첫 번째 그래프 설명
# ------------------------------------------------------------

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 적어 보세요.",
    placeholder="예: 개봉 직후 관객 수가 많고 시간이 지나면서 관객 수가 감소하는 것을 알 수 있다.",
    height=100,
    key="graph1_note"
)


# ============================================================
# 2. 일관객 합계 TOP 5 영화의 날짜별 변화
# ============================================================

st.divider()

st.header("2. 일관객 합계가 가장 큰 TOP 5 영화")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편을 골라 날짜별 일관객 변화를 비교합니다."
)


# ------------------------------------------------------------
# 전체 기간 일관객 합계 계산
# ------------------------------------------------------------

top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

top5_names = top5_movies["영화명"].tolist()


# ------------------------------------------------------------
# TOP 5 영화의 날짜별 데이터
# ------------------------------------------------------------

top5_df = df[
    df["영화명"].isin(top5_names)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


# ------------------------------------------------------------
# 두 번째 그래프
# ------------------------------------------------------------

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>"
                  "날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,.0f}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    height=650,
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ------------------------------------------------------------
# 두 번째 그래프 설명
# ------------------------------------------------------------

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 적어 보세요.",
    placeholder="예: 영화마다 일관객 수가 가장 높아지는 시점과 감소하는 속도가 다르다는 것을 알 수 있다.",
    height=100,
    key="graph2_note"
)


# ============================================================
# 3. 날짜별 전체 10위권 일관객 합계
# ============================================================

st.divider()

st.header("3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜에 박스오피스 10위권에 기록된 영화들의 일관객을 모두 더해 "
    "하루 전체 관객 규모가 어떻게 변화했는지 확인합니다."
)


# ------------------------------------------------------------
# 날짜별 10위권 일관객 합계 계산
# ------------------------------------------------------------

daily_audience = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


# ------------------------------------------------------------
# 일관객 합계가 가장 큰 날짜 TOP 3
# ------------------------------------------------------------

top3_days = (
    daily_audience
    .sort_values("일관객", ascending=False)
    .head(3)
)


# ------------------------------------------------------------
# 세 번째 영역 그래프
# ------------------------------------------------------------

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x=daily_audience["날짜"],
        y=daily_audience["일관객"],
        mode="lines",
        fill="tozeroy",
        name="10위권 일관객 합계",
        hovertemplate=
            "날짜: %{x|%Y-%m-%d}<br>"
            "10위권 일관객 합계: %{y:,.0f}명"
            "<extra></extra>"
    )
)


# ------------------------------------------------------------
# TOP 3 날짜 표시
# ------------------------------------------------------------

for _, row in top3_days.iterrows():

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=(
            f"{row['날짜'].strftime('%Y-%m-%d')}"
            f"<br>{row['일관객']:,.0f}명"
        ),
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-60
    )


fig3.update_layout(
    title="날짜별 박스오피스 10위권 일관객 합계",
    xaxis_title="날짜",
    yaxis_title="일관객 합계(명)",
    height=600,
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# ------------------------------------------------------------
# 세 번째 그래프 설명
# ------------------------------------------------------------

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 적어 보세요.",
    placeholder="예: 날짜에 따라 영화관을 찾은 관객 수가 크게 달라지며, 특정 날짜에 전체 관객 수가 집중되는 것을 알 수 있다.",
    height=100,
    key="graph3_note"
)


# ============================================================
# 4. 다음 그래프를 추가할 공간
# ============================================================

st.divider()

st.header("4. 다음 그래프")

st.info(
    "앞으로 새로운 그래프를 추가할 때 이 구역 아래에 "
    "그래프와 '이 그래프로 알 수 있는 것' 부분을 추가하면 됩니다."
)


# ============================================================
# 데이터 정보
# ============================================================

st.divider()

st.header("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "전체 기록 수",
        f"{len(df):,}개"
    )

with col2:
    st.metric(
        "기록된 영화 수",
        f"{df['영화명'].nunique():,}편"
    )

with col3:
    st.metric(
        "데이터 기간",
        f"{df['날짜'].min().strftime('%Y-%m-%d')} ~ "
        f"{df['날짜'].max().strftime('%Y-%m-%d')}"
    )
