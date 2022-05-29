FROM python:3.10.4-slim-buster
WORKDIR /app
COPY . .
CMD ["python", "sort_manager.py", "/home"]
