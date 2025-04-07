# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables for Docker environment
ENV DB_HOST=postgres-db
ENV DB_PORT=5432
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASSWORD=admin

# Start the application
CMD ["python", "-m", "backend.run"] 