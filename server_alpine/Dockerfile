FROM alpine:3.16.2
LABEL maintainer="eggs2017"

ARG ssh_user
ARG ssh_pass
ARG synchDir

RUN apk add openssh
RUN apk add rsync
RUN apk add openssh-keygen


#add user
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config
RUN adduser -h /home/${ssh_user} -s /bin/sh -D ${ssh_user}
RUN echo -n ${ssh_user}:${ssh_pass} | chpasswd

#create synchdir
RUN mkdir ${synchDir} && chown ${ssh_user} ${synchDir}

COPY init.sh /
RUN chmod 775 /init.sh
ENTRYPOINT ["sh", "/init.sh"]

EXPOSE 22
