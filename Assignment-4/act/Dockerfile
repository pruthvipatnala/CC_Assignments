from alpine:3.7
RUN apk add --no-cache python3-dev && pip3 install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip3 --no-cache-dir install -r requirements.txt
EXPOSE 5000
ENV TEAM_ID=CC_188_249_012
ENTRYPOINT ["./entrypoint.sh"]