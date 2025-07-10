FROM python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "bot.py"]