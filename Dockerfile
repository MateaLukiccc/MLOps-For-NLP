FROM python:3.11-slim

ENV POETRY_VERSION=1.8.5
ENV POETRY_HOME=/opt/poetry
ENV POETRY_CACHE_DIR=/opt/.cache

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry export --without-hashes --dev -f requirements.txt > requirements.txt \
    && pip install --timeout=300 --no-cache-dir -r requirements.txt --index-url https://pypi.org/simple \
    && rm requirements.txt

RUN pip install torch==2.0.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY . /app

EXPOSE 8000

CMD ["python", "api/app.py"]
