import streamlit as st
import requests

API_KEY = "여기에_본인_TMDB_API_KEY_입력"

def search_movie(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}&language=ko-KR"
    response = requests.get(url)
    results = response.json().get("results")
    return results

def get_movie_credits(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json()

def get_recommendations_by_person(person_id):
    url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={API_KEY}&language=ko-KR"
    response = requests.get(url)
    return response.json()

def main():
    st.title("🎬 TMDb 기반 영화 추천 앱")

    movie_name = st.text_input("영화 제목 입력")

    if movie_name:
        results = search_movie(movie_name)
        if not results:
            st.warning("검색 결과가 없습니다.")
            return

        # 첫 번째 영화 선택
        movie = results[0]
        st.write(f"검색된 영화: {movie['title']} ({movie['release_date'][:4] if movie.get('release_date') else 'N/A'})")

        credits = get_movie_credits(movie["id"])
        director = None
        for crew_member in credits.get("crew", []):
            if crew_member["job"] == "Director":
                director = crew_member
                break

        actors = credits.get("cast", [])[:5]  # 상위 5명 배우

        st.write(f"감독: {director['name'] if director else '정보 없음'}")
        st.write("주요 배우:")
        for actor in actors:
            st.write(f"- {actor['name']}")

        # 감독 영화 추천
        if director:
            st.write(f"🎥 감독 {director['name']}의 다른 작품:")
            director_credits = get_recommendations_by_person(director["id"])
            director_movies = [m for m in director_credits.get("crew", []) if m["job"] == "Director" and m["id"] != movie["id"]]
            for m in director_movies[:5]:
                st.write(f"- {m['title']} ({m.get('release_date', '')[:4]})")

        # 배우 영화 추천
        st.write("🎭 주요 배우들의 다른 작품:")
        for actor in actors:
            st.write(f"배우 {actor['name']}의 작품:")
            actor_credits = get_recommendations_by_person(actor["id"])
            actor_movies = [m for m in actor_credits.get("cast", []) if m["id"] != movie["id"]]
            for m in actor_movies[:3]:
                st.write(f"- {m['title']} ({m.get('release_date', '')[:4]})")

if __name__ == "__main__":
    main()
