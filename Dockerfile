FROM python:3.7.3-slim

ENV LANG  en

WORKDIR /dirPencarian

COPY pencarian/. .

RUN pip install --upgrade pip


# djanggo
RUN pip install django==3.2.18

# backend env
RUN pip install numpy==1.16.2
RUN pip install pandas==0.24.2
RUN pip install urllib3==1.26.2
RUN pip install scipy==1.2.1

RUN pip install simplemma==0.5.0
RUN pip install nltk==3.4
RUN pip install typing-extensions==3.7.4.3
RUN pip install spacy==3.0.6
RUN pip install scikit-learn==0.20.3


CMD "python" "manage.py" "runserver" "0.0.0.0:8080"

