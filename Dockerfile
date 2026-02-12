FROM python:3.11-slim

# Базовые настройки
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Устанавливаем минимальные инструменты сборки для C-расширений (psutil и др.)
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём venv и ставим зависимости в него
RUN python3 -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Копируем проект
COPY . /app/project/
WORKDIR /app/project

# Обновляем pip/wheel и ставим зависимости проекта
RUN /app/.venv/bin/pip install --no-cache-dir -U pip wheel \
    && /app/.venv/bin/pip install --no-cache-dir -e .

# Делаем install.sh исполняемым
RUN chmod +x /app/project/install.sh

# Entrypoint: запускаем install.sh в неинтерактивном режиме, затем приложение
ENTRYPOINT ["/bin/bash", "-c", "/app/project/install.sh --non-interactive 2>/dev/null || true && /app/.venv/bin/python -m shop_bot"]