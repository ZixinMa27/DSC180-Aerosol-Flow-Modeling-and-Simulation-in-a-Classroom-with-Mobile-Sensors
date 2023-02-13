FROM ucsdets/datahub-base-notebook

USER root

RUN pip install --no-cache-dir -r requirements.txt
