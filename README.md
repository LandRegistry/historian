# Historian

[![Build Status](https://travis-ci.org/LandRegistry/historian.svg)](https://travis-ci.org/LandRegistry/historian)

Storing of versioned data.

## Description

Storage pluggable, currently S3, with FileSystem support soon.

### Common

Configure

    PORT=xxxx
    HOST="http://example.org/"

### S3

Configure

    export AWS_ACCESS_KEY_ID=YOUR_KEY
    export S3_BUCKET='some-bucket-name'
    export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET

If the bucket doesn't exist, ensure the ```AWS``` credential has permissions to create it. If you create it beforehand, ensure the bucket has versioning support.

## How to use

    pip install -r requirements
    ./run.py


### Create

    curl -X POST
      -H "Content-Type: application/json"
      http://localhost:8015/a/b/c/123
      -d '{"foo": "bar", "other": "stuff",  "answer": 42 }'

....and again


    curl -X POST
      -H "Content-Type: application/json"
      http://localhost:8015/a/b/c/123
      -d '{"foo": "barium", "other": "stuffing",  "answer": 43 }'


The storage will map the path ```a/b/c/123``` to a resource:
- S3: file 123 in path <bucket>/a/b/c
- FileSystem: file 123 in subdirectory /a/b/c

### Read


    curl -H "Accept: application/json"
      http://localhost:8015/a/b/c/123

...which will return the original (and latest version of the) content, as well as meta-data about the resource.

### Versions

    curl -H "Accept: application/json"
      http://localhost:8015/a/b/c/123?versions=list

...which will return an array of meta-data about the resource.

### Specific version

    curl -H "Accept: application/json"
      http://localhost:8015/a/b/c/123?version=a-specific-version

...which will return the specific version of the content, as well as meta-data about the resource.


