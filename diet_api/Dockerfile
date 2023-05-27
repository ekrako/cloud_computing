FROM python:3.11-alpine
COPY requierments.txt /tmp/requierments.txt
RUN pip3 install --no-cache-dir -r /tmp/requierments.txt && rm /tmp/requierments.txt
COPY . /app
WORKDIR /app
EXPOSE 5002
CMD ["python3", "main.py"]
