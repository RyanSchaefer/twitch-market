# Index
Welcome to Twitch Market documentation. This page will serve as a guide for myself and others who wish to delve into the code behind Twitch Market. 

## Index
### [Commands](https://vsquiddevv.github.io/twitch-market/commands/)
What the user can send to Twitch Market.
### [Database](https://vsquiddevv.github.io/twitch-market/database/)
Requests from the clients to the database server.
### [Server](https://vsquiddevv.github.io/twitch-market/server/)
The machine that connects to Twitch and hands out messages to clients.
### [Tests](https://vsquiddevv.github.io/twitch-market/tests/)
Offline testing of Twitch Market
### [Twitch Connection](https://vsquiddevv.github.io/twitch-market/twitch_communication/)
Connection to Twitch.
### [Users](https://vsquiddevv.github.io/twitch-market/users/)
How user data is stored.

## Overview
We will begin with a diagram that explains how Twitch market works:

![](https://www.websequencediagrams.com/cgi-bin/cdraw?lz=cGFydGljaXBhbnQgVHdpdGNoIGFzIHQKAAwMU2VydmVyIGFzIHMACw1Xb3JrIFF1ZXVlIGFzIHdvcmsAEQ5oaXNwZXIAFwtxAEoNQ2xpZW50IGFzIGMAYg1EYXRhYmFzAFAFZAAEFgBsCWRxCnMtPit0OiBzb2NrZXQuY29ubmVjdChbdACBSAVdKQpsb29wIGZvciBlYWNoIGMAcAUKYy0-czoAIxBzAIFjBV0pCmVuZAp0LT5zOiB3AIE-BgpzLT53b3JrOgCBYQVfcXVldWUucHV0KAAZBykKd29yay0-K2MAFQ1nZQAXC29wAIFQC1JlcXVlc3RzCiAgICBjLT5kAHwRZACBfwddKVxuc2VuZF9tZXNzYWdlKAARCCwgcgA_BikAQAVkLT5kcToAUQggYWRkZWQgdG8gAIEnBQAcBnEtPmQAGApwcm9jZXNzZWQANwhjOlJlc291cmNlIHJldHVybmVkAIIFBWMAgXQITQB8BgAVCSAocGFyc2VkKQpkZWFjdGl2YXRlIGMAggQHczogAIJKBiBwdWxscyBmcm9tAIEGB29wdCBTZW5kIACBTAcgdG8gAIMpBgCCCgVzLT53cTogaWYAgnYIIGluIGxpc3QocGF5bG9hZACBawZ3cQCDFgwAgmcKAIIJBnMtPnQ6AIEpCHNlbnQAg1AFAIEdC3QK&s=default)

Now this might be a lot to take in but I will break it down.

1. The main server connects to Twitch.
2. Each client connects to the main server.
3. The main server receives a whisper and puts it into its work queue.
4. The server then sends it to a client that is not currently processing a request.
5. The client then parses the message for possible commands.
  
	Optionally - 
	1. The client connects to the database and makes a request.
	2. The database finds the resource or alters it.
	3. The database returns the resource or a Boolean depending on the request.

6. The client returns a command to the server.
7. The main server processes commands sequentially
	
	Optionally -
	1. A request to send a whisper is added to the queue
	2. The request is pulled from the queue
	3. The message is sent
	4. The main server must wait for a message limit posed by Twitch until it can send another message
