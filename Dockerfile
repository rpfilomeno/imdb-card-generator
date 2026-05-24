# Use the official Astral UV environment layer 
FROM astral-sh/uv:python3.11-alpine

# Set context working workspace
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first to leverage Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using the lockfile (omit project root install since it is a script)
RUN uv sync --frozen --no-install-project

# Copy single script asset across tracking branches
COPY main.py .

# Expose standard default Streamlit communication port
EXPOSE 8501

# Prevent python internal script memory buffering
ENV PYTHONUNBUFFERED=1

# Instruct UV to run the script inside the synced virtual environment
ENTRYPOINT ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]