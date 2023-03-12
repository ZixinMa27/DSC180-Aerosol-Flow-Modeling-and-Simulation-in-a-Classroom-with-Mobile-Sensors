FROM ucsdets/datahub-base-notebook

USER root

COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install --no-cache-dir -r "requirements.txt"
