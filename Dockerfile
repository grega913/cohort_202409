FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/streamlit/streamlit-example.git .



WORKDIR /app/src

COPY . /app/src

# RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -U python-dotenv

EXPOSE 8501

#GCP
EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health



# ENTRYPOINT ["streamlit", "run", "src/streamlit_multipage.py", "--server.port=8501", "--server.address=0.0.0.0"]

ENTRYPOINT ["streamlit", "run", "src/streamlit_multipage.py", "--server.port=8080", "--server.address=0.0.0.0"]