FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure usage_stats.json exists so Flask can read/write
RUN echo '{"files_processed": 0, "products_updated": 0, "images_added": 0, "total_usage_count": 0}' > /app/usage_stats.json

EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
