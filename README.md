# Superheroes API

## Description
A Flask REST API for tracking superheroes and their superpowers.  
Heroes can have many powers, and powers can belong to many heroes through hero powers.

## Setup Instructions

1. Clone the repository
2. Install dependencies
3. Run migrations
4. Seed the database
5. Start the server

```bash
pipenv install
pipenv shell
flask db upgrade
python seed.py
flask run

