# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /code

# システム依存ライブラリ
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# 依存パッケージコピー & インストール
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ソースコピー
COPY . .

