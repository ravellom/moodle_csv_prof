FROM python:3.9-alpine

# Install build dependencies
RUN apk update
RUN apk add --no-cache --virtual .tmp make automake gcc g++ subversion python3-dev postgresql-dev linux-headers

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies
RUN apk del .tmp

# Install runtime dependencies
RUN apk add --no-cache libstdc++

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

CMD [ "/entrypoint.sh" ]