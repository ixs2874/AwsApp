# AwsApp
<h2>Basic Publishing Service</h2>
This code uses Chalice serverless microframework to build a simple publishing service. 

<h3> System requirements </h3>
<p> 
1. Python 3.6  (python -V)<br>
2. git 3.8 (git --version)<br>
3. pip 9 (pip --version)<br>
</p>
<h3> Setup steps for Linux RH</h3>
<p>
mkdir test<br>
cd test<br>
git clone https://github.com/ixs2874/AwsApp <br>
mkdir ~/.aws<br>
mv ./config ~/.aws/<br>
python -m venv venv<br>
. ./venv/bin/activate<br>
pip install -r requirements.txt<br>
chalice deploy<br>
</p>

<h2> Service Methods</h2>
1. --------------------------------------------------------------------------<br>
To get server status execute the following command:<br>
http https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/status<br>
Note: to use http command install httpie, which is part of requirements.txt<br>
AWS Gateway routs /status endpoint to status() function. Function collects system timestemp, os/platform data and returns it as dictionary.<br><br>
2. ---------------------------------------------------------------------------<br>
This package contains 2 sample images under /chalicelib directory to be uploaded at S3 AWS storage.<br> 
Steps to upload images to S3 execute the following commands:<br>

homer1="$(base64 -i `pwd`/chalicelib/Homer_artwork.png)"<br>
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer1)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img<br><br>

homer2="$(base64 -i `pwd`/chalicelib/homer_doh.jpg)"<br>
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer2)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img<br><br>
<h4>Description for image uploade service</h4>
<p>
base64 command encodes an image into stream and assigns it variable "homerX".<br>
curl posts "homerX" image to "post/img" endpoint on AWS Lambda service and returns URL of the image on S3.<br>
Chalice server forwards post/img Post request to post_image() function, reads json payload, decodes image, uses ImageMagick convert command and pubprocess.Popen function to creat thumbnail img, then thumbnail is uploaded to S3 ixs2874 bucket and URL is returned.<br>
</p>

