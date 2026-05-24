import re
import os
import streamlit as st
import streamlit.components.v1 as components
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page Configurations
st.set_page_config(
    page_title="Offline TMDB Component Generator",
    page_icon="🎬",
    layout="wide"
)

# Bundled Tailwind CSS Core Layer Build String
TAILWIND_OFFLINE_CORE = r"""
*,::after,::before{box-sizing:border-box;border-width:0;border-style:solid;border-color:theme(borderColor.DEFAULT, currentColor)}
html{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;tab-size:4;font-family:ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-feature-settings:normal;font-variation-settings:normal}
body{margin:0;line-height:inherit}
.flex{display:flex}
.flex-col{flex-direction:column}
.grid{display:grid}
.items-center{align-items:center}
.items-end{align-items:end}
.justify-center{justify-content:center}
.justify-between{justify-content:space-between}
.min-h-screen{min-height:100vh}
.bg-black{background-color:#000}
.bg-white{background-color:#fff}
.mx-auto{margin-left:auto;margin-right:auto}
.p-4{padding:1rem}
.py-3{padding-top:0.75rem;padding-bottom:0.75rem}
.py-2{padding-top:0.5rem;padding-bottom:0.5rem}
.px-5{padding-left:1.25rem;padding-right:1.25rem}
.pt-2{padding-top:0.5rem}
.mt-4{margin-top:1rem}
.rounded-3xl{border-radius:1.5rem}
.rounded-t-3xl{border-top-left-radius:1.5rem;border-top-right-radius:1.5rem}
.shadow-xl{box-shadow:0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)}
.shadow-sm{box-shadow:0 1px 2px 0 rgb(0 0 0 / 0.05)}
.max-w-\\[270px\\]{max-width:270px}
.w-full{width:100%}
.h-56{height:14rem}
.h-14{height:3.5rem}
.h-5{height:1.25rem}
.object-cover{object-fit:cover}
.font-bold{font-weight:700}
.font-black{font-weight:900}
.font-semibold{font-weight:600}
.font-light{font-weight:300}
.text-2xl{font-size:1.5rem;line-height:2rem}
.text-3xl{font-size:1.875rem;line-height:2.25rem}
.text-sm{font-size:0.875rem;line-height:1.25rem}
.text-xs{font-size:0.75rem;line-height:1rem}
.text-slate-900{color:#0f172a}
.text-slate-700{color:#334155}
.text-slate-400{color:#94a3b8}
.text-slate-300{color:#cbd5e1}
.text-yellow-500{color:#eab308}
.tracking-wider{letter-spacing:0.05em}
.leading-relaxed{line-height:1.625}
.gap-x-1{column-gap:0.25rem}
.gap-x-2{column-gap:0.5rem}
.line-clamp-2{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden}
.line-clamp-3{display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden}
a{text-decoration:inherit;color:inherit}
.group:hover .group-hover\:text-cyan-700{color:#0e7490}
.group:hover .group-hover\:text-yellow-600{color:#ca8a04}
"""

COMPONENT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        {tailwind_css}
    </style>
</head>
<body class="bg-black flex items-center justify-center m-0 p-4">
    <div class='mx-auto bg-white rounded-3xl shadow-xl max-w-[270px]'>
         <div class="rounded-3xl shadow-sm bg-white">
          <img
             src="{cover_url}"
             class="rounded-t-3xl justify-center h-56 w-full object-cover"
             alt="{title}"
          /> 

          <div class="group px-5 py-3 grid z-10">
            <a
              href="https://www.imdb.com/title/{imdb_id}/"
              class="group-hover:text-cyan-700 font-bold text-2xl line-clamp-2 text-slate-900"
              target="_blank"
            >
              {title}
            </a>
            <span class="text-slate-400 pt-2 font-semibold"> 
              ({year})
            </span>
            <div class="h-14">
              <span class="line-clamp-3 py-2 h-14 leading-6 text-sm font-light leading-relaxed text-slate-700">
                {plot}
              </span>
            </div>
            <div class="grid-cols-2 flex group justify-between mt-4">
              <div class="font-black flex flex-col">
                <div class="text-yellow-500 text-xs tracking-wider">TMDB SCORE</div>
                <div class="text-3xl flex gap-x-1 items-center group-hover:text-yellow-600 text-slate-900">
                 {rating}
                 <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9.15316 5.40838C10.4198 3.13613 11.0531 2 12 2C12.9469 2 13.5802 3.13612 14.8468 5.40837L15.1745 5.99623C15.5345 6.64193 15.7144 6.96479 15.9951 7.17781C16.2757 7.39083 16.6251 7.4699 17.3241 7.62805L17.9605 7.77203C20.4201 8.32856 21.65 8.60682 21.9426 9.54773C22.2352 10.4886 21.3968 11.4691 19.7199 13.4299L19.2861 13.9372C18.8096 14.4944 18.5713 14.773 18.4641 15.1177C18.357 15.4624 18.393 15.8341 18.465 16.5776L18.5306 17.2544C18.7841 19.8706 18.9109 21.1787 18.1449 21.7602C17.3788 22.3417 16.2273 21.8115 13.9243 20.7512L13.3285 20.4768C12.6741 20.1755 12.3469 20.0248 12 20.0248C11.6531 20.0248 11.3259 20.1755 10.6715 20.4768L10.0757 20.7512C7.77268 21.8115 6.62118 22.3417 5.85515 21.7602C5.08912 21.1787 5.21588 19.8706 5.4694 17.2544L5.53498 16.5776C5.60703 15.8341 5.64305 15.4624 5.53586 15.1177C5.42868 14.773 5.19043 14.4944 4.71392 13.9372L4.2801 13.4299C2.60325 11.4691 1.76482 10.4886 2.05742 9.54773C2.35002 8.60682 3.57986 8.32856 6.03954 7.77203L6.67589 7.62805C7.37485 7.4699 7.72433 7.39083 8.00494 7.17781C8.28555 6.96479 8.46553 6.64194 8.82547 5.99623L9.15316 5.40838Z" fill="#eab308"/> 
                 </svg>
                </div>
              </div>
              <div class="flex flex-col items-end">
                <div class="h-5" />
                <span class="text-3xl font-bold gap-x-2 text-slate-300">
                  {popularity_rank}
                </span>
              </div>
          </div>
        </div>
        </div>
    </div>
</body>
</html>
"""

def extract_id(input_string):
    match = re.search(r'(tt\d+)', input_string)
    return match.group(1) if match else None

def fetch_from_tmdb(imdb_id, api_key):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}"
    params = {"api_key": api_key, "external_source": "imdb_id"}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
        
    res_data = response.json()
    media_data = None
    
    if res_data.get("movie_results"):
        media_data = res_data["movie_results"][0]
        title = media_data.get("title")
        release_date = media_data.get("release_date", "N/A")
        year = release_date.split("-")[0] if release_date != "N/A" else "N/A"
    elif res_data.get("tv_results"):
        media_data = res_data["tv_results"][0]
        title = media_data.get("name")
        first_air_date = media_data.get("first_air_date", "N/A")
        year = first_air_date.split("-")[0] if first_air_date != "N/A" else "N/A"
        
    if not media_data:
        return None

    poster_path = media_data.get("poster_path")
    cover_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=500"
    
    vote_average = media_data.get("vote_average", 0.0)
    rating = f"{round(vote_average, 1)}" if vote_average else "N/A"
    
    popularity = media_data.get("popularity", 0.0)
    pop_rank = f"#{int(popularity)}" if popularity else ""

    return {
        "title": title,
        "year": year,
        "plot": media_data.get("overview", "No plot outline provided by TMDB."),
        "rating": rating,
        "cover_url": cover_url,
        "popularity_rank": pop_rank
    }

# App Layout
st.title("🎬 UV Powered TMDB Component Generator")
st.markdown("Uses `uv` execution mechanics to manage self-contained Python runtimes and local inline CSS styles.")

st.divider()

tmdb_key = os.getenv("TMDB_API_KEY", "")

user_input = st.text_input(
    "IMDb Destination ID or Complete URL", 
    placeholder="e.g. tt42178219"
)

if user_input:
    if not tmdb_key:
        st.warning("Please provide your TMDB API Key inside the .env file as TMDB_API_KEY.")
    else:
        imdb_id = extract_id(user_input)
        if not imdb_id:
            st.error("Could not parse a valid identifier pattern (ttXXXXXXX).")
        else:
            with st.spinner("Calling TMDB discovery instances directly..."):
                try:
                    movie_data = fetch_from_tmdb(imdb_id, tmdb_key)
                    
                    if movie_data:
                        rendered_html = COMPONENT_TEMPLATE.format(
                            tailwind_css=TAILWIND_OFFLINE_CORE,
                            imdb_id=imdb_id,
                            title=movie_data["title"],
                            year=movie_data["year"],
                            plot=movie_data["plot"],
                            rating=movie_data["rating"],
                            cover_url=movie_data["cover_url"],
                            popularity_rank=movie_data["popularity_rank"]
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("📋 Output Source Script (Self-Contained)")
                            st.code(rendered_html, language="html", line_numbers=True)

                        with col2:
                            st.subheader("👀 Component Render Sandbox")
                            components.html(rendered_html, height=520, scrolling=False)
                            
                    else:
                        st.error(f"No corresponding profile item mapping found for ID: `{imdb_id}`")
                except Exception as e:
                    st.error(f"Internal processing exception: {str(e)}")