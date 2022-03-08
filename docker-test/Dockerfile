FROM alpine
RUN apk update && apk add --update python3 py3-pip && apk add curl

COPY ./script.sh /app/script.sh
WORKDIR /app

CMD ["./script.sh"]