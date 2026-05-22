import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

st.title("📈 그래프 예시")
st.write("matplotlib, seaborn, plotly를 사용한 그래프 예시입니다. 모든 그래프의 제목과 축은 한글로 표시됩니다.")


from pathlib import Path
import matplotlib.font_manager as fm

font_path = Path(__file__).resolve().parent.parent / "fonts" / "NotoSansKR-ExtraBold.ttf"
plt.rcParams["axes.unicode_minus"] = False
font_name = None

if font_path.exists():
    try:
        font_props = fm.FontProperties(fname=str(font_path))
        fm.fontManager.addfont(str(font_path))
        font_name = font_props.get_name()
        plt.rcParams["font.family"] = font_name
        st.write(f"**사용 중인 한글 폰트:** {font_name}")
    except Exception as e:
        st.warning(f"한글 폰트를 로드하는 중 오류가 발생했습니다: {e}")
else:
    st.warning("fonts/NatoSansKR-ExtraBold.ttf 파일을 찾을 수 없습니다. 폰트 파일을 확인해 주세요.")

st.header("1. matplotlib 막대 그래프")
bar_data = pd.DataFrame({
    "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
    "판매량": [120, 180, 150, 210, 190, 230],
})
fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(bar_data["월"], bar_data["판매량"], color="#4C72B0")
ax1.set_title("월별 판매량", fontsize=16)
ax1.set_xlabel("월")
ax1.set_ylabel("판매량 (개)")
for idx, value in enumerate(bar_data["판매량"]):
    ax1.text(idx, value + 5, str(value), ha="center")
st.pyplot(fig1)

st.header("2. seaborn 선 그래프")
line_data = pd.DataFrame({
    "날짜": pd.date_range(start="2026-05-01", periods=7, freq="D"),
    "기온": [18, 20, 22, 19, 21, 23, 24],
})
line_data["날짜"] = line_data["날짜"].dt.strftime("%m월 %d일")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.lineplot(data=line_data, x="날짜", y="기온", marker="o", ax=ax2, color="#DD8452")
ax2.set_title("일별 평균 기온", fontsize=16)
ax2.set_xlabel("날짜")
ax2.set_ylabel("기온 (℃)")
ax2.grid(True, linestyle="--", alpha=0.4)
st.pyplot(fig2)

st.header("3. plotly 파이 차트")
pie_data = pd.DataFrame({
    "연령대": ["10대", "20대", "30대", "40대", "50대 이상"],
    "비율": [15, 35, 28, 14, 8],
})
fig3 = px.pie(
    pie_data,
    names="연령대",
    values="비율",
    title="연령대별 사용자 비율",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig3.update_traces(textposition="inside", textinfo="percent+label")
fig3.update_layout(
    title_font_size=18,
    legend_title_text="연령대",
    font_family=font_name or "sans-serif",
)
st.plotly_chart(fig3, use_container_width=True)

st.header("4. plotly 산점도 예시")
scatter_data = pd.DataFrame({
    "매출": [200, 250, 180, 300, 270, 320, 290],
    "광고비": [40, 50, 35, 60, 55, 65, 58],
    "분류": ["A", "B", "A", "C", "B", "C", "A"],
})
fig4 = px.scatter(
    scatter_data,
    x="광고비",
    y="매출",
    color="분류",
    size="매출",
    title="광고비 대비 매출 산점도",
    labels={"광고비": "광고비 (만원)", "매출": "매출 (만원)"},
)
fig4.update_layout(font_family=font_name or "sans-serif")
st.plotly_chart(fig4, use_container_width=True)
