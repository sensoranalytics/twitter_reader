Twitter Reader
==============

This application simulates the behavior of an RFID reader, but using Twitter. It "reads" the 'mentions' for a given Twitter
account then generates an SMF (Savi Sensor Message Format) message and sends it to Savi for processing.

##Run on dev box
```sh
python fetch_mentions.py
```
##Run Unit Tests
```sh
nosetests
```

##Install Requirements
```sh
pip install -r requirements.txt
```

##Sample Supervisor configuration
```sh
[program:twitter_reader]
command = /home/deploy/virtual_envs/twitter_reader/bin/python /home/deploy/twitter_reader/mentions_reader.py
stdout_logfile=/var/log/mentions.log
stderr_logfile=/var/log/mentions.log
autostart = True
autorestart = True
```