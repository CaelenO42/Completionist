<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/CaelenO42/Completionist">
    <img src="img/logo_full.svg" alt="Logo" width="300" height="auto">
  </a>
  <p align="center">
    A Flask app for simple task management, categorization, and filtering
    <br />
    <p align="center">
      <a href="https://github.com/caeleno42/Completionist/graphs/contributors"><img src="https://img.shields.io/github/contributors/caeleno42/Completionist.svg" alt="Contributors Shield"></a>
      <a href="https://github.com/caeleno42/Completionist/issues"><img src="https://img.shields.io/github/issues/caeleno42/Completionist.svg" alt="Issues Shield"></a>
    </p>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#windows">Windows</a></li>
        <li><a href="#linux">Linux</a></li>
        <li><a href="#macos">MacOS</a></li>
        <li><a href="#configure-redis">Configure Redis</a></li>
        <li><a href="#setting-up-mailersend">Setting up Mailersend</a></li>
        <li><a href="#setting-up-postgresql">Setting up PostgreSQL</a></li>
        <li><a href="#run-flask-app">Run Flask App</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#top-contributors">Top Contributors</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

A simple app using Flask, PostgreSQL, and Redis to allow users to log in and create, delete, filter, categorize, and complete tasks.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![HTML][HTML]][HTML-url]
* [![SCSS][SCSS]][SCSS-url]
* [![JavaScript][JavaScript]][JavaScript-url]
* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![Redis][Redis]][Redis-url]
* [![Postgres][Postgres]][Postgres-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Clone the repository

```bash
git clone git@github.com:CaelenO42/Completionist.git
cd Completionist
```

### Windows
<details>
<br>

Redis is not offically supported on Windows so you will need to set up an Ubuntu version of WSL2, instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install). After successfulyl installing WSL, follow the [Linux](#linux) instructions.

</details>

### Linux
<details>

#### Setup a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Install Redis

```bash
sudo apt install redis-server
```

</details>

### MacOS
<details>

#### Setup a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Install Redis
Installing Redis on macOS requires Homebrew which you can install [here](https://brew.sh/)

```bash
brew install redis
```

</details>

### Configure Redis

```bash
sudo nano /etc/redis/redis.conf
```
* In the ```redis.conf``` file, change the line ```supervised no``` to ```supervised systemd```.


### Setting up Mailersend
*Mailersend is used to send out our Email Verification and Password Reset emails*

Create a [mailersend account](https://www.mailersend.com/) and generate an API Token.
Once you have your token open your `.env` file and add the following:

```yaml
MAILERSEND_API_KEY = "{{YOUR MAILERSEND API KEY HERE}}"
```

### Setting up PostgreSQL

1. Install [PostgreSQL](https://www.postgresql.org/download/) for your operating system. \
For MacOS you could also use something like [Postgres.app](https://postgresapp.com/)

1. Run the ```setup_db.py``` script located in ```database/``` to create the database and tables in the database.

### Run Flask app

1. Add values to your `.env` file

```yaml
FLASK_APP=src
FLASK_ENV=development
```

2. Run app

```bash
flask run
```

3. Open app url in browser `http://127.0.0.1:5000` or `localhost:5000`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Figma UI design
  - [ ] Home Page
  - [x] Main Task View
  - [ ] Sign In / Sign Up
  - [ ] User Settings
- [ ] Setup Flask environment
- [ ] Implement pages
  - [ ] Home page
    * This page should tell the user what the app is and prompt them to create an account
  - [ ] Main Task View
    - [ ] Create Tasks
    - [ ] Remove Tasks
    - [ ] Change Task Status
    - [ ] Change Task Due Date
    - [ ] Change Task Category
    - [ ] Drag to reorder tasks
    - [ ] Filter tasks
  - [ ] Sign In / Sign Up
  - [ ] Edit user profile page
    * This page allows users to update their profile information
- [ ] Database
  - [ ] Database Conceptual Design
  - [ ] Database Schema
  - [ ] Setup PostgreSQL server
- [ ]

See the [open issues](https://github.com/caeleno42/Completionist/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Top Contributors

<a href="https://github.com/caeleno42/Completionist/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=caeleno42/Completionist" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/caeleno42/Completionist.svg?style=for-the-badge
[contributors-url]: https://github.com/caeleno42/Completionist/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/caeleno42/Completionist.svg?style=for-the-badge
[issues-url]: https://github.com/caeleno42/Completionist/issues

[JavaScript]: https://img.shields.io/badge/javascript-000000?style=for-the-badge&logo=javascript
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML]: https://img.shields.io/badge/html5-000000?style=for-the-badge&logo=html5
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[SCSS]: https://img.shields.io/badge/SCSS-000000?style=for-the-badge&logo=sass
[SCSS-url]: https://sass-lang.com/
[Redis]: https://img.shields.io/badge/Redis-000000?style=for-the-badge&logo=redis
[Redis-url]: https://redis.io/
[Python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
[Flask]: https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Postgres]: https://img.shields.io/badge/postgresql-000000?style=for-the-badge&logo=postgresql
[Postgres-url]: https://www.postgresql.org/
