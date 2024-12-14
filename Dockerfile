FROM python:3.11-slim

# Configure Poetry
ENV POETRY_VERSION=1.8.5
ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry
RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

# Copy poetry files and install dependencies
COPY poetry.lock pyproject.toml ./

# Export dependencies to requirements.txt and install them globally using pip
RUN poetry export --without-hashes --dev -f requirements.txt > requirements.txt \
    && pip install --timeout=300 --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple \
    && rm requirements.txt

# Install PyTorch in the system environment
RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Copy application code
COPY . /app

# Run your app directly
CMD ["python", "app.py"]
