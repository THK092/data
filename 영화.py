import streamlit as st

# 영화 데이터: 영화명 -> 감독, 배우 리스트, 간단 줄거리(옵션)
movies = {
    "인셉션": {
        "director": "크리스토퍼 놀란",
        "actors": ["레오나르도 디카프리오", "조셉 고든-레빗", "엘런 페이지"],
        "summary": "꿈 속 꿈을 탐험하는 이야기."
    },
    "다크 나이트": {
        "director": "크리스토퍼 놀란",
        "actors": ["크리스찬 베일", "히스 레저", "애런 에크하트"],
        "summary": "배트맨과 조커의 대결."
    },
    "셔터 아일랜드": {
        "director": "마틴 스코세이지",
        "actors": ["레오나르도 디카프리오", "마크 러팔로", "베니치오 델 토로"],
        "summary": "정신병원에서 벌어진 미스터리."
    },
    "어벤져스": {
        "director": "조스 웨던",
        "actors": ["로버트 다우니 주니어", "크리스 에반스", "스칼렛 요한슨"],
        "summary": "히어로들이 모여 세상을 구한다."
    },
    "아이언맨": {
        "director": "존 파브로",
        "actors": ["로버트 다우니 주니어", "그윈네스 팰트로", "테렌스 하워드"],
        "summary": "억만장자 발명가의 슈트 이야기."
    },
    "토르": {
        "director": "케네스 브래너",
        "actors": ["크리스 헴스워스", "톰 히들스턴", "나탈리 포트만"],
        "summary": "천둥의 신 토르의 모험."
    },
    "인터스텔라": {
        "director": "크리스토퍼 놀란",
        "actors": ["매튜 맥커너히", "앤 해서웨이", "제시카 차스테인"],
        "summary": "우주 탐사를 통한 인류 구원."
    },
    "라라랜드": {
        "director": "다미엔 차젤레",
        "actors": ["라이언 고슬링", "엠마 스톤"],
        "summary": "재즈 음악가와 배우의 사랑 이야기."
    },
    "기생충": {
        "director": "봉준호",
        "actors": ["송강호", "이선균", "조여정"],
        "summary": "계층 간의 충돌과 반전."
    },
    "겨울왕국": {
        "director": "크리스 벅",
        "actors": ["이디나 멘젤", "크리스틴 벨"],
        "summary": "자매의 사랑과 마법 이야기."
    },
    # 여기에 50~100개 더 추가 가능 (용량 제한 주의)
}

def recommend(movie_title):
    if movie_title not in movies:
        return None
    director = movies[movie_title]["director"]
    actors = movies[movie_title]["actors"]

    recommendations = []
    for m, info in movies.items():
        if m == movie_title:
            continue
        # 감독이 같거나 배우가 하나라도 겹치면 추천
        if info["director"] == director or any(actor in info["actors"] for actor in actors):
            recommendations.append({
                "title": m,
                "director": info["director"],
                "actors": info["actors"],
                "summary": info.get("summary", "")
            })
    return recommendations

def main():
    st.title("🎬 풍부한 정보가 담긴 영화 추천 앱")
    st.write("영화 제목 입력 시 감독 및 배우가 겹치는 다른 작품과 간단 줄거리를 추천합니다.")

    movie_input = st.text_input("영화 제목 입력 (예: 인셉션, 어벤져스, 기생충)")

    if movie_input:
        recs = recommend(movie_input)
        if recs is None:
            st.warning("데이터에 없는 영화입니다. 다른 제목으로 시도해 주세요.")
        elif len(recs) == 0:
            st.info("추천할 영화가 없습니다.")
        else:
            st.success(f"'{movie_input}'와 관련된 추천 영화들:")
            for r in recs:
                st.markdown(f"### {r['title']}")
                st.write(f"감독: {r['director']}")
                st.write(f"출연 배우: {', '.join(r['actors'])}")
                st.write(f"줄거리: {r['summary']}")
                st.write("---")

if __name__ == "__main__":
    main()
