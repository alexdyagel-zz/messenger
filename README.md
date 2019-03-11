# Nostromo
Nostromo is a great messenger which allows you to communicate through network with your friends.
### Installation
Nostromo's server requires [sqlalchemy](https://www.sqlalchemy.org/), [bcrypt](https://pypi.org/project/bcrypt/) for valid run.
Installing example: 
```sh
$ pip install bcrypt
$ pip install SQLAlchemy
```
Or using requirements file:
```sh
$ pip install -r /path/to/requirements.txt
```

### Run Nostromo

First of all you should run server. Server package can be placed in any host separately from client.
You should run messenger_server.py script which stored in server package root. 
There are two optional arguments:
* --ip
* --port

If they are not specified, default values will be chosen (current host ip address and 8080 for ip and port respectively).
Examples of running server:
```sh
$ python messenger_server.py
$ python messenger_server.py --ip 127.0.0.1
$ python messenger_server.py --ip 192.168.56.5 --port 8081
```

Then you should run client-side messenger. You should run messenger.py script which stored in root of client package. Script requires 4 arguments:
* --ip (ip address of server)
* --port (port of server)
* --login (login of user)
* --password (password of user)

Example of running messenger:
```sh
$ python messenger.py --ip 127.0.0.1 --port 8080 --login sasha --password 12345
```

When you successfully launched messenger you can communicate with others. By default you send broadcast messeges. To send messege to a certain user use this template:
```sh
@user_login message
```
To quit from messenger type:
```sh
[quit]
```

