FROM python:3.11

WORKDIR /app

# now should be in the working dir
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copy over the py file - don't think need anything else
COPY app.py .

# run the command - equiv to python -m flask run
CMD ["python", "-m",  "flask",  "run", "--host=0.0.0.0"]
