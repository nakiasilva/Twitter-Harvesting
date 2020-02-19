
""" Installation for Docker """

1. Configure /etc/enviornment file
	cat /etc/environment 
	http_proxy="http://wwwproxy.unimelb.edu.au:8000"
	https_proxy="http://wwwproxy.unimelb.edu.au:8000"
	ftp_proxy="http://wwwproxy.unimelb.edu.au:8000"
	no_proxy=localhost,127.0.0.1,127.0.1.1,ubuntu

2. Set up the repository 
	sudo yum install -y yum-utils \
	  device-mapper-persistent-data \
	  lvm2

	sudo yum-config-manager \
	    --add-repo \
	    https://download.docker.com/linux/centos/docker-ce.repo

3. Install Docker CE
	sudo yum install docker-ce docker-ce-cli containerd.io


4. Configure HTTP/HTTPS proxy

	sudo mkdir -p /etc/systemd/system/docker.service.d
	vi /etc/systemd/system/docker.service.d/http-proxy.conf
		[Service]
		Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000"

	vi /etc/systemd/system/docker.service.d/https-proxy.conf
		[Service]
		Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000"

5. Flush Changes
	
	sudo systemctl daemon-reload
	sudo systemctl restart docker

6. Pull couchDB image
	docker pull couchdb:2.3.0
