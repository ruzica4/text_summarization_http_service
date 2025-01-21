FROM python:3.10-slim

WORKDIR /app
ENV FLASK_ENV=development 
# ENV NLTK_DATA=/usr/local/share/nltk_data

COPY requirements3.txt /app/
RUN pip install --no-cache-dir -r requirements3.txt
# RUN python -c "import nltk; nltk.download('punkt')"
# RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt stopwords wordnet omw-1.4 reuters
COPY . /app
EXPOSE 5000

CMD ["python", "src/app.py"]