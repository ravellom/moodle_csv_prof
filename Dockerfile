FROM python:3.9

# Install build dependencies
RUN apt update && apt upgrade

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

CMD [ "/entrypoint.sh" ]