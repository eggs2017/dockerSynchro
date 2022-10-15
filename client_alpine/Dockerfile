FROM alpine:3.16.2


RUN apk add openssh
RUN apk add sshpass
RUN apk add rsync

COPY ssh_user.pass  /
COPY synchDir.sh /
COPY scheduler_rsync.txt /

RUN chmod +x /ssh_user.pass /synchDir.sh

ADD entrypoint.sh /
RUN chmod 775 /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]