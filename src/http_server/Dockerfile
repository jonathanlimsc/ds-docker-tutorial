## Note: Build context dir: docker-tutorial/. Execute docker build -t http_server -f ./src/http_server/Dockerfile . to build image/
## Execute docker run -it -p 10000:10000 http_server to run image.

# Base image
FROM python:3.6

# Create working directory workdir
RUN mkdir workdir/
WORKDIR workdir/

# Install python packages (earlier == good)
COPY ./src/http_server/requirements.txt ./
RUN pip install -r requirements.txt

# Create src and http_server dir to mirror code repo
RUN mkdir src/
RUN mkdir src/http_server

# Copy files to http_server dir
COPY ./src/http_server/* src/http_server/

# Change working directory to model_server
WORKDIR src/http_server/

# Expose port 10000
EXPOSE 10000

# Start server script
CMD python http_server.py
