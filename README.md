# AwsApp
<h2>Basic Publishing Service</h2>
This code uses Chalice serverless microframework to build a simple publishing service. 

<h3> System requirements </h3>
<p> 
1. Python 3.6  (python -V)
2. git 3.8 (git --version)
3. pip 9 (pip --version)
</p>
<h3> Setup steps in linux environment </h3>
<p>
git clone https://github.com/ixs2874/AwsApp
mkdir ~/.aws
mv ./config ~/.aws/
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
chalice deploy
</p>


1. To get status execute the following:
http https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/status

2. This project contains 2 sample images under /chalicelib that could be uploaded to S3 AWS storage. 

To upload image to S3 execute the following commands:

<code>
homer1="$(base64 -i `pwd`/chalicelib/Homer_artwork.png)"

curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer1)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img


homer2="$(base64 -i `pwd`/chalicelib/homer_doh.jpg)"

curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer2)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img
</code>
