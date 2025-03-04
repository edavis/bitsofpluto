FROM python:3.12-slim
WORKDIR /app
COPY bitsofpluto.py /app/
RUN pip install --no-cache-dir pillow atproto
CMD ["python", "bitsofpluto.py"]
