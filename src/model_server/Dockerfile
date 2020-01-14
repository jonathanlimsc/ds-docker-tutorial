## Note: Build context dir: docker-tutorial/. Execute docker build -t model_server -f ./src/model_server/Dockerfile . to build image
## Execute docker run -it model_server to run image.

# Base image
FROM python:3.6

# Create working directory workdir
RUN mkdir workdir/
WORKDIR workdir/

# Install python packages (earlier == good)
COPY ./src/model_server/requirements.txt ./
RUN pip install -r requirements.txt

# Create src, model_server and model dirs to mirror code repo
RUN mkdir src/
RUN mkdir src/model_server
RUN mkdir model

# Copy files to model_server dir
COPY ./src/model_server/* src/model_server/

# Copy model weights
COPY ./model/model.pkl model/

# Change working directory to model_server
WORKDIR src/model_server/

# Start server script
CMD python model_server.py
