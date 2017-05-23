# AwsApp
<h2>Basic Publishing Service</h2>
This code uses Chalice serverless microframework to build a simple publishing service. 

<h3> System requirements </h3>
<p> 
1. Python 3.6  (python -V)<br>
2. git 3.8 (git --version)<br>
3. pip 9 (pip --version)<br>
</p>
<h3> Setup steps in linux environment </h3>
<p>
git clone https://github.com/ixs2874/AwsApp <br>
mkdir ~/.aws<br>
mv ./config ~/.aws/<br>
python -m venv venv<br>
. ./venv/bin/activate<br>
pip install -r requirements.txt<br>
chalice deploy<br>
</p>


1. To get status execute the following:<br>
http https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/status

2. This project contains 2 sample images under /chalicelib that could be uploaded to S3 AWS storage.<br> 
Steps to upload images to S3 execute the following commands:<br>
<code>
homer1="$(base64 -i `pwd`/chalicelib/Homer_artwork.png)"<br>
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer1)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img<br><br>

homer2="$(base64 -i `pwd`/chalicelib/homer_doh.jpg)"<br>
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer2)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img<br>
</code>
