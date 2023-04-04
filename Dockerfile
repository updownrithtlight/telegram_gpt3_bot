# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY telegram_gpt3_bot.py .

# Expose the port on which the bot will run (optional)
EXPOSE 8080

# Define
# Define the environment variables for API keys
ENV TELEGRAM_API_TOKEN=your-telegram-api-token
ENV OPENAI_API_KEY=your-openai-api-key

# Set the command to run the Python script
CMD ["python", "telegram_gpt3_bot.py"]
