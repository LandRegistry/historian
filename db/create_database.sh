#!/bin/bash

createuser -s historian
createdb -U historian -O historian historian -T template0
