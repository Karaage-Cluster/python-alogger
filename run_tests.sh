#!/bin/bash
DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

RETURN=0
cd $DIR

echo ""
echo "FLAKE8"
echo "############################"
flake8 alogger
if [ ! $? -eq 0 ]
then
    RETURN=1
fi

echo ""
echo "TESTS"
echo "############################"
export TZ='Australia/Melbourne'
py.test alogger
if [ ! $? -eq 0 ]
then
    RETURN=1
fi

exit $RETURN
