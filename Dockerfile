# start by pulling the python image
FROM python:3.10-slim

# copy the requirements file into the image
COPY ./requirements.txt /code/requirements.txt

# switch working directory
WORKDIR /code

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy every content from the local file to the image
COPY . /code

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["run.py" ]