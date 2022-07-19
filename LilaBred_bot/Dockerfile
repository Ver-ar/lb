FROM python:3.9
ENV POETRY_VERSION=1.1.13
RUN pip install "poetry==$POETRY_VERSION"

ENV PATH="/root/.local/bin:$PATH"
WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-dev --no-root
COPY . /code
RUN poetry config virtualenvs.in-project true --local

CMD ["poetry", "run", "python", "main.py"]