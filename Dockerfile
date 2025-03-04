FROM python:3.12-slim
WORKDIR /app
COPY bitsofpluto.py /app/
COPY data/crop_p_color2_enhanced_release.png /app/
RUN pip install --no-cache-dir pillow atproto
CMD ["python", "bitsofpluto.py"]
