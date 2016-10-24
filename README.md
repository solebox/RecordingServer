# Recording Server

this is essentially a recording microservice that uses ffmpeg to record 
video from any url ffmpeg can get as input, recordings can be scheduled 
and authentication is done using hmac PSK mechanism.
both server and client need to sync clocks or else the timestamp would 
invalidate the HMAC signature 
