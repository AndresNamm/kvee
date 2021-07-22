# Note: You can use any Debian/Ubuntu based image you want. 
FROM mcr.microsoft.com/vscode/devcontainers/python:3.8


COPY src/ /var/task/
COPY Pipfile /var/task/
COPY Pipfile.lock /var/task/ 

RUN pipenv install --system --deploy