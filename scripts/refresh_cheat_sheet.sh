# install acme
curl https://get.acme.sh | sh -s email=my@example.com

# get a cert
acme.sh --issue -d "*.baidu.com" --dns dns_azure

# install cert to nginx
mkdir -p /etc/nginx/ssl/baidu.com/
acme.sh --install-cert -d baidu.com \
--key-file       /etc/nginx/ssl/baidu.com/key.pem  \
--fullchain-file /etc/nginx/ssl/baidu.com/cert.pem \
--reloadcmd     "nginx -s reload"