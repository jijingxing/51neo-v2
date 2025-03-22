FROM alpine
WORKDIR /app
COPY . /app
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk update
RUN apk add python3 && \
pip install -r requirements.txt --break-system-packages && \
echo '#!/bin/sh' > ./launch.sh && \
echo 'python3 ./app.py' >> ./launch.sh && \
rm ./Dockerfile && \
chmod +x ./launch.sh
CMD [ "./launch.sh" ]
