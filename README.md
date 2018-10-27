# backend

Backend za studentski projekat na RAFu, na predmetu "Skript jezici".

## Production enviroment

We have this app deployed on [our own server](https://skript-api.nemanja.top/). 

## TOC

<!-- vim-markdown-toc GFM -->

* [Getting started](#getting-started)
* [Code style](#code-style)
	* [Installing python virtual environment](#installing-python-virtual-environment)
	* [Installing deps in virtual environment](#installing-deps-in-virtual-environment)
	* [Database](#database)
		* [Login](#login)
		* [Running DB using docker (docker-compose)](#running-db-using-docker-docker-compose)
		* [Importing schema](#importing-schema)
	* [Helpers](#helpers)
		* [Timetable import](#timetable-import)
		* [User import](#user-import)
		* [Fast database reset and import](#fast-database-reset-and-import)

<!-- vim-markdown-toc -->

## Getting started

## Code style

For maintaining the same code style, across different code editors, we are using [EditorConfig](https://editorconfig.org/)... 

There is `.editorconfig` file present in the root of the project. 

### Installing python virtual environment

```bash
./devscripts/install_environment.sh
```
### Installing deps in virtual environment

```bash
./devscripts/install_dependencies.sh
```

### Database

#### Login

Password for root user should be `example`. 

#### Running DB using docker (docker-compose)

```bash
cd ./db
docker-compose up
```

#### Importing schema

```bash
python3 manage.py migrate
```

### Helpers

#### Timetable import

```bash
python3 ./parser.py
```

#### User import

```bash
python3 ./student_data.py
```

#### Fast database reset and import

```bash
./devscripts/reset_db.sh
```

