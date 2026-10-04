# Best Cars Dealership — Full-Stack Capstone

Best Cars is a responsive full-stack dealership review application created for
the IBM Full-Stack Development Capstone. Visitors can browse dealership
branches throughout the United States, filter them by state, inspect details
and sentiment-tagged reviews, create accounts, and publish purchase reviews.

## Technology

- Django and SQLite for authentication, administration, car makes, and models
- Responsive HTML/CSS/JavaScript interface with React component source
- Node.js, Express, MongoDB, and Mongoose dealership microservice source
- Flask sentiment-analysis microservice
- Docker, Kubernetes, GitHub Actions, and Gunicorn deployment configuration

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
cd server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Open <http://127.0.0.1:8000/dealers>. The seeded demonstration account is
`demo` with password `DemoPass123!`.

## Main API routes

- `POST /djangoapp/login`
- `GET /djangoapp/logout`
- `POST /djangoapp/register`
- `GET /djangoapp/get_dealers`
- `GET /djangoapp/get_dealers/Kansas`
- `GET /djangoapp/dealer/8`
- `GET /djangoapp/reviews/dealer/8`
- `GET /djangoapp/get_cars`
- `POST /djangoapp/add_review`

## Quality and deployment

GitHub Actions runs Django validation, migrations, and tests on each push. The
included Dockerfile and Kubernetes manifest package the app for cloud-native
deployment.
