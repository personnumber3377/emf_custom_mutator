#!/bin/sh
cd ../emf_parser/
./test.sh
# ../emf_parser/test.sh

cd ../emf_custom_mutator/

cp ../emf_parser/*.py . # Copy the sources from the parser to this directory...
cp -r ../emf_parser/cparsing/ .
python3 mutator.py # Try to run the mutator tests...


