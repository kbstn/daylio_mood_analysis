# try to pull slim images to avoid big image sizes
FROM python:3.8.4-slim

# port to expose the container on 
EXPOSE 8505

# The WORKDIR instruction sets the working directory (FOR WITHIN THE IMAGE) for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile . Let’s set it to app/ :
WORKDIR /app

# # # # this is only if we want to clone via git
# potential fix for error 100: https://stackoverflow.com/questions/38002543/apt-get-update-returned-a-non-zero-code-100
# RUN apt-get update && apt-get install -y apt-transport-https
# RUN apt-get install -y \
#    build-essential \
#    software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/kbstn/daylio_mood_analysis.git .

COPY . .

# install the python libs listet in txt file taht we copied into /app folder
RUN pip3 install -r requirements.txt


ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8505", "--server.address=0.0.0.0"]


