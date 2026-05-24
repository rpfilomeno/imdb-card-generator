# IMDb Card Generator 🎬

A Streamlit web application that generates visually appealing, self-contained HTML/CSS cards for IMDb movies and TV shows using the TMDB API. The generated components use inline Tailwind CSS and are completely offline-ready, making them easy to embed anywhere.

## ✨ Features

- **TMDB Integration**: Automatically fetches movie/show details, posters, ratings, and popularity using just an IMDb ID (e.g., `tt42178219`).
- **Self-Contained Components**: Generates a single HTML snippet with bundled CSS and JavaScript. No external dependencies are required to render the card once generated.
- **Image Export**: Easily download the card as a high-resolution PNG or copy it directly to your clipboard.
- **Docker Support**: Fully containerized and ready to run using Docker Compose.

## 🚀 Getting Started

### Prerequisites

You will need a TMDB API Key to fetch movie data.
1. Get a free API key from [The Movie Database (TMDB)](https://www.themoviedb.org/documentation/api).
2. Copy the `.env.example` file to `.env` and add your API key:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` and set `TMDB_API_KEY=your_api_key_here`.*

### Running Locally (with uv)

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

```bash
# Run the Streamlit application
uv run streamlit run main.py
```

### Running with Docker

You can easily run the application using Docker Compose without needing to set up a local Python environment.

```bash
# Build and start the container
docker-compose up -d
```

The app will be available at `http://localhost:8501`.

## 📖 Usage

1. Open the application in your browser.
2. Enter an IMDb ID (e.g., `tt0111161` for The Shawshank Redemption) or the full IMDb URL.
3. The app will fetch the details and render the card.
4. You can view the generated HTML code, copy the image, or download it as a PNG.