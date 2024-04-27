FROM ubuntu

RUN apt-get update

# Avoid tzdata infinite waiting bug
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Africa/Cairo
RUN apt-get update --fix-missing
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install python3 libapache2-mod-wsgi-py3
RUN apt-get install -y graphviz libgraphviz-dev pkg-config
RUN ln /usr/bin/python3 /usr/bin/python
RUN apt-get -y install python3-pip
#Add sf to avoid ln: failed to create hard link '/usr/bin/pip': File exists
RUN ln -sf /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip --break-system-packages
RUN pip install django ptvsd --break-system-packages
RUN pip install autopep8 --break-system-packages
RUN apt install wait-for-it
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt --break-system-packages
ADD ./site.conf /etc/apache2/sites-available/000-default.conf
EXPOSE 80
WORKDIR /var/www/html
#CMD ["apache2ctl", "-D", "FOREGROUND"]
#CMD ["python", "manage.py", "migrate", "--no-input"]
