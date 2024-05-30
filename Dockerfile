FROM ubuntu:latest
WORKDIR /app
# update
RUN apt-get update
# install python
RUN apt-get install -y python3 pip
# install python dependencies
RUN pip install flask flask_cors flask_caching requests beautifulsoup4 pyopenssl
# copy files
COPY api.py /app
COPY rozklad_jazdy.py /app
COPY index.html /app/templates/
COPY rozklad.html /app/templates/
COPY manifest.json /app/static/
COPY export.geojson /app/static/

CMD ["python3", "api.py"]