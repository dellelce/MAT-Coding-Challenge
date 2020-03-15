FROM mclarenappliedtechnologies/recruitment.fanengagement.forwarder:latest
COPY app.sh /
RUN chmod +x /app.sh

#ENTRYPOINT ["java" "-Djava.security.egd=file:/dev/./urandom" "-jar" "/app.jar"]
ENTRYPOINT ["/bin/sh", "/app.sh"]
