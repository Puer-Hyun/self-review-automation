#!/bin/bash

url=$1
start=$2
end=$3
self_review_number=$4

# gradio 실행, 인자를 전달
python 'gradio/app.py' $self_review_number &

# Selenium 코드 실행
python self_review.py $url $start $end $self_review_number