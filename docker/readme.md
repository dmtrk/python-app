#Connector docker
##Installing docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

##Running
- create config file
docker secret create imap-2-http-client1.cfg file example/imap-2-http-client1.cfg


openssl genrsa -out key.pem 2048

- start connector:
`docker-compose up -d`

- stopping:  
`docker-compose down`
