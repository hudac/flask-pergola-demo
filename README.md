# A Todo List demo App
This is a todo list demo, including howto deploy to [Pergola](https://pergola.cloud).
It is based on the original tutorial from [@tcheng10](https://tichung.com/blog/2021/20200323_flask/).


## Requirements
* Python >= 3.8
* Docker >= 18
* Access to a Pergola platform


## Getting started

### Setup Git repository
Before you can push your changes, you need your own Git repository Pergola has read access to
(e.g. a public [repository on GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)).

In this example, `hudac/flask-pergola-demo` is the new repository.
```bash
# clone from this repository
git clone https://github.com/datasophie/flask-pergola-demo.git
cd flask-pergola-demo

# push to my repository
git remote set-url origin git@github.com:hudac/flask-pergola-demo.git
git push
```

### Pergola manifest
Create a `pergola.yaml` file in the root folder with the following content:
```yaml
version: v1

components:
- name: todo-app
  docker:
    file: Dockerfile
  ports:
  - 5050
  ingresses:
  - host: app
  env:
  - name: SQLALCHEMY_HOST
    component-ref: todo-db
  - name: SQLALCHEMY_PORT
    value: "5432"
  - name: SQLALCHEMY_DB
    value: flask-demo
  - name: SQLALCHEMY_USER
    config-ref: DB_USER
  - name: SQLALCHEMY_PASSWORD
    config-ref: DB_PASS

- name: todo-db
  docker:
    image: postgres:14.12
  env:
  - name: POSTGRES_DB
    value: flask-demo
  - name: POSTGRES_USER
    config-ref: DB_USER
  - name: POSTGRES_PASSWORD
    config-ref: DB_PASS
  storage:
  - name: pgdata
    path: /var/lib/postgresql/data
    size: 1Gi
  ports:
  - 5432
```

Push `pergola.yaml` to your repository:
```bash
git add pergola.yaml
git commit -m 'pergola manifest added'
git push
```

### Setup project and push first release to Pergola
*Note:* For public repositories use the `https` Git url.
```bash
# project: pergola-demo-todo-app
pergola create project pergola-demo-todo-app \
  --display-name "Pergola Demo ToDo App" \
  --git-url "https://github.com/hudac/flask-pergola-demo.git"

# trigger a build manually, we don't want to wait
pergola push build -p pergola-demo-todo-app

# stage: dev
pergola create stage dev --type dev -p pergola-demo-todo-app

# add configuration: default
# to stage: dev
# hint: generate a password if you don't need to know it upfront (and avoids leaving a trace in shell history)
pergola add config-data default -s dev -p pergola-demo-todo-app \
  --env DB_USER=flask-demo \
  --env DB_PASS=$(cat /dev/urandom | env LC_ALL=C tr -dc '[:alnum:]' | head -c21)

# check if newest build is ready
pergola list build -p pergola-demo-todo-app

# push a new release
# build: main_b1 (assuming main_b1 is the newest)
# with config: default
# to stage: dev
pergola push release -b main_b1 -c default -s dev -p pergola-demo-todo-app

# check running application and open generated url
pergola list component -s dev -p pergola-demo-todo-app
```

Whenever you have a new build, just issue `pergola push release`. Everything else is already setup.

## Running the app locally (debugging)

### With Python
*Note:* You need `pg_config` installed which is available in `postgresql-devel` (`libpq-dev` in Debian/Ubuntu,
`libpq-devel` on Centos/Fedora).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

### With Docker
```bash
docker compose build
docker compose up
```
