## Note: Build context dir: docker-tutorial/. Execute docker build -t simple_model_server -f ./src/simple_model_server/Dockerfile . to build image/
## Execute docker run -it -p 10000:10000 simple_model_server to run image.

# Base image
FROM python:3.6

# Create working directory workdir
RUN mkdir workdir/
WORKDIR workdir/

# Install python packages (earlier == good)
COPY ./src/simple_model_server/requirements.txt ./
RUN pip install -r requirements.txt

# Create src, model_server and model dirs to mirror code repo
RUN mkdir src/
RUN mkdir src/model_server
RUN mkdir model

# Copy files to model_server dir
COPY ./src/simple_model_server/* src/model_server/

# Copy model weights
COPY ./model/model.pkl model/

# Change working directory to model_server
WORKDIR src/model_server/

# Install python packages (later == bad)
# RUN pip install -r requirements.txt

# Expose port 10000
EXPOSE 10000

# Start server script
CMD python simple_model_server.py
