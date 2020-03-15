# Test for Edited
#
FROM alpine:3.9

LABEL maintainer="Antonio Dell'Elce"

ENV LANG  en_GB.utf8

COPY src/ /scripts/

RUN apk add --no-cache mysql mysql-client mariadb-backup pwgen && \
    mkdir /run/mysqld && chown mysql /run/mysqld && \
    rm /etc/my.cnf.d/mariadb-server.cnf

# Do NOT mix ini parameters and command options
ENTRYPOINT ["/scripts/run.sh"]
