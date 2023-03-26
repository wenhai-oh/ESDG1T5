FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./central_reservation_system.py ./invokes.py ./
CMD [ "python", "./central_reservation_system.py" ]