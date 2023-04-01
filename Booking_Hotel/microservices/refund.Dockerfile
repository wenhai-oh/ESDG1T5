FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt stripe
COPY ./flask_stripe/flask_stripe/refund.py ./
CMD [ "python", "./refund.py" ]