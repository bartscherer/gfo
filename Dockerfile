FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL maintainer="Thomas Bartscherer <thomas@bartscherer.io>"
COPY gfo/requirements.txt /tmp/requirements.txt
COPY gfo /app
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
RUN chmod +x prestart.sh process_wrapper.sh
CMD ["/bin/bash", "process_wrapper.sh"]