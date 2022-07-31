FROM python:3.10.5

RUN pip install -U pip 
RUN pip install pipenv
ADD . .
RUN pipenv install --system --deploy --ignore-pipfile