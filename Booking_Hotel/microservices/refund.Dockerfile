FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r stripe_req.txt
# COPY ./flask_stripe/flask_stripe/refund.py ./
COPY ./refund.py ./
CMD [ "python", "./refund.py" ]