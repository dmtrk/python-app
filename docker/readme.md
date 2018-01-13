#Connector docker
##Installing docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

##Building
`docker-compose build` will create an image in local docker repo

##Running
- create config file
docker secret create imap-2-http-client1.cfg example/client1.cfg

- create ssl key and cert
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 3650 -nodes

- create service:
`docker service  create --name imap-2-http-client1 --secret imap-2-http-client1.cfg imap-2-http-connector:latest`


$(cd src/main/resources && protoc --python_out=../../../src/main/python/ bytes-message.proto)