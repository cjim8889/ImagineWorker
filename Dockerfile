ARG BASE_IMAGE=huggingface/transformers-pytorch-gpu:4.28.1
FROM ${BASE_IMAGE} as dev-base

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    python3-opencv

# Copy everything
COPY . /app

WORKDIR /app

# Install required Python packages
RUN python3 -m pip install --upgrade pip && \
    pip3 install -r requirements.txt

# Set the working directory
WORKDIR /app/components/CodeFormer

RUN pip3 install -r requirements.txt && \
    python3 basicsr/setup.py develop

WORKDIR /app

RUN python3 setup.py

# Set the entry point
ENTRYPOINT ["python3", "-u", "main.py"]
