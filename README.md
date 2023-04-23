# docker-test
sample project with docker and python. Just for my own tinkering nothing to see here

## notes on local setup
faffing around getting the wsl setup too me about half the time...
https://learn.microsoft.com/en-us/windows/wsl/setup/environment
install wsl on local windows - note this just installed as root unlike ms docs say. I didn't bother creating a non-root user
```
wsl install
sudo apt update && sudo apt upgrade
```
install docker (just downloaded)
python3 was on there already but installed 3.11
```bash
sudo apt install python3.11-full
```

also had to reconfigure git via the following
```
git config --global --edit
```
later on to push had to use a PAT from github
finally created a dev dir, created a new repo and cloned
opened vs code via "code ." in the working dir

## python env and flask app
very basic setup as per app.py
set up the venv and freeze the requirements
```bash
python3.11 -m venv venv --prompt .
```
install flask and freeze the dependencies

## dockerize flask app
Primarily following the first link

https://docs.docker.com/language/python/
https://docs.docker.com/language/python/build-images/

 after creating the dockerfile build the image
```bash
docker build --tag python-docker-test .
```
above command takes a bit of time as it's the full (not slim) python and ends up being ~1gb

then to run it
```bash
docker run --publish 8000:5000 python-docker-test
```

at this point can see running in docker desktop and connect via localhost:8000. It will have been given a name

to run it in detached mode, providing a name
```docker
docker run -d -p 8000:5000 --name python-flask-docker python-docker-test
```
you can see everything in the docker desktop gui, or via commands
```docker
docker image ls
docker container ls
```
use docker stop/start (docker restart will stop (if running) and start)

## database piece
 run db in a different container, but use mounts to keep data outside of the container
 and so can persist outside the life of the container
 going for postgres rather than mysql
 https://hub.docker.com/_/postgres/
 https://www.howtogeek.com/devops/how-to-deploy-postgresql-as-a-docker-container/


create the volume
```docker
docker volume create postgres_data
docker volume ls
```

note if you don't create a volume, running the postgres container did create an anonymous volume

create a docker network so both containers can communicate

```docker
docker network create my-app-network
docker network ls
```

now run the postgres container. the -rm flag will just remove the instance after it's stopped. -e is just an environment variable. Without specifying a version of postgres it just gets the latest (for a version, would have e.g. postgres:15 instead of postgres)
```docker
docker run --rm -d --name my_postgres --network my-app-network -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=passw0rd postgres
```

can interact with the db using psql...
```docker
docker exec -it my_postgres psql -U postgres
```

pip install psycopg2-binary

running the instance now with -rm so that it's removed once shut down
```
docker run -d --rm -p 8000:5000 --name python-flask-docker-dev --network my-app-network python-docker-test`
```

curl http://localhost:8000/initdatabase


in psql, connect to the inventory db, list the tables
```sql
\connect inventory;
\dt;
select * from widgets;
```

## create compose file
the compose file has all the info to run both containers but all in a single file to run
```
docker compose -f docker-compose.dev.yml up --build
```

note that the containers then run as part of an overarching docker-test container
```
docker container ls
```
|CONTAINER ID|IMAGE|COMMAND|CREATED|STATUS|PORTS|NAME|
|---|---|---|---|---|---|---|
|43a49b4474d7|docker-test-web|"python -m flask run…"|5 minutes ago|Up 5 minutes|0.0.0.0:8000->5000/tcp| docker-test-web-1|
|fe26056647cd|postgres|"docker-entrypoint.s…"|5 minutes ago|Up 5 minutes|0.0.0.0:5432->5432/tcp|docker-test-my_postgres-1|
