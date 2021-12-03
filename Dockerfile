FROM python:3.9

RUN apt update && apt upgrade

WORKDIR /app

# Make staticfiles dir
RUN mkdir /static

# Make sqlite database location
RUN mkdir /etc/data

COPY requirements.txt .
RUN pip install --no-cache-dir wheel && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 29000

CMD [ "/entrypoint.sh" ]