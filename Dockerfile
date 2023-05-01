ARG BASE_IMAGE=nvcr.io/nvidia/l4t-pytorch:r35.2.1-pth2.0-py3
FROM ${BASE_IMAGE} as dev-base

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    python3-opencv

# Copy everything
COPY . /app

WORKDIR /app

# Install required Python packages
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the working directory
WORKDIR /app/app/components/CodeFormer

RUN pip install -r requirements.txt && \
    python basicsr/setup.py develop

WORKDIR /app/app

RUN python setup.py

# Set the entry point
ENTRYPOINT ["python", "-u", "main.py"]
