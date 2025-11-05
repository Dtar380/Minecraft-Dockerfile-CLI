FROM eclipse-temurin:21-jdk-jammy

ENV SERVER_DIR=/server
ENV SERVER_JAR=server.jar
ENV JAVA_ARGS=""
ENV MIN_HEAP_SIZE=""
ENV MAX_HEAP_SIZE=""

WORKDIR $SERVER_DIR

COPY scripts/run.sh /usr/local/bin/run.sh
RUN chmod +x /usr/local/bin/run.sh

ENTRYPOINT ["/usr/local/bin/run.sh"]
