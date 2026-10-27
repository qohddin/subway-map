import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. 앱 제목 및 설명 설정
st.title("🚇 부산 지하철 역별 이용객 수 지도 분석 앱")
st.markdown("`busan_subway.csv` 파일을 업로드하면 지도 위에 이용객 수에 비례하는 원형 마커가 표시됩니다.")

# 2. CSV 파일 업로드 기능
uploaded_file = st.file_uploader("busan_subway.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 업로드된 파일을 판다스 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터를 표 형태로 화면에 출력
    st.subheader("📋 업로드된 데이터 미리보기")
    st.dataframe(df.head())

    # [추가 기능] 호선별 색상 지정 딕셔너리
    color_dict = {
        '1호선': 'orange',
        '2호선': 'green',
        '3호선': 'brown',
        '4호선': 'blue'
    }

    # [추가 기능] multiselect로 호선 필터링
    unique_lines = df['호선'].unique()
    selected_lines = st.multiselect("지도를 확인할 호선을 선택하세요:", unique_lines, default=unique_lines)

    # 선택된 호선만 남기도록 데이터프레임 필터링 적용
    df = df[df['호선'].isin(selected_lines)]

    # 3. Folium 지도 객체 생성 (부산 중심 좌표 기준)
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)

    # 4. 데이터프레임의 행을 하나씩 읽으며 지도에 CircleMarker 추가
    for index, row in df.iterrows():
        # 원의 면적이 이용객 수에 비례하도록 반지름에 제곱근 적용
        radius = (row['이용객수'] ** 0.5) * 0.15

        # 딕셔너리에서 해당 호선의 색상 가져오기 (해당 없으면 회색)
        marker_color = color_dict.get(row['호선'], 'gray')

        # CircleMarker 추가 (마우스 호버 시 역명, 클릭 시 이용객 수 설정)
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.6,
            tooltip=row['역명'],
            popup=f"이용객수: {row['이용객수']:,}명"
        ).add_to(m)

    # 5. Streamlit 화면에 지도 렌더링
    st.subheader("🗺️ 부산 지하철 이용객 수 지도 시각화")
    st_folium(m, width=700, height=500)

    # [추가 기능] 이용객 상위 5개 역 표 표시
    st.subheader("🏆 이용객 수 상위 5개 역")
    # 이용객수 기준으로 내림차순 정렬 후 상위 5개 추출
    top5_df = df.sort_values(by='이용객수', ascending=False).head(5)
    # 필요한 열만 선택하고 인덱스를 리셋하여 깔끔하게 출력
    st.dataframe(top5_df[['호선', '역명', '이용객수']].reset_index(drop=True))

else:
    # 파일이 업로드되지 않았을 때 안내 메시지
    st.warning("⚠️ 상단에서 `busan_subway.csv` 파일을 먼저 업로드해 주세요.")