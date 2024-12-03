# Use a Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code into the container
COPY . .

# Expose port 5000 (common for web apps, not needed in this case, but safe to have)
EXPOSE 5000

# Command to run the bot
CMD ["python", "bot.py"]
