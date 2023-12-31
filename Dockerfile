# Use an official Python runtime as a parent image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY ./requirements.txt ./app/requirements.txt
# COPY ./app /app/app
COPY . .

# Install any needed packages specified in requirements.txt
# RUN pip install openai==0.10.2
# RUN pip install httpx==0.13.0
RUN apt-get update && \
    apt-get install -y ffmpeg
RUN apt-get install flac
RUN pip install googletrans==4.0.0rc1
RUN apt-get update && \
    apt-get install -y libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev
RUN pip install PyAudio
RUN pip install --no-cache-dir -r ./app/requirements.txt
# RUN import httpcore
# RUN setattr(httpcore, 'SyncHTTPTransport', 'AsyncHTTPProxy')



# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV OPENAI_API_KEY="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"

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
