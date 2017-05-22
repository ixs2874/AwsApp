# AwsApp
Basic Publishing Service:
This code uses Chalice serverless microframework to build a simple publishing service. 

1. To get status execute the following:
http https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/status

2. This project contains 2 sample images under /chalicelib that could be uploaded to S3 AWS storage. 

To upload image to S3 execute the following commands:
homer1="$(base64 -i `pwd`/chalicelib/Homer_artwork.png)"
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer1)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img

homer2="$(base64 -i `pwd`/chalicelib/homer_doh.jpg)"
curl -X POST -H "Content-Type: application/json" -d '{ "width": 128, "height": 128, "format": "PNG", "data": "'"$(echo $homer2)"'"}' https://i04vs3m4ch.execute-api.us-east-1.amazonaws.com/dev/post/img
