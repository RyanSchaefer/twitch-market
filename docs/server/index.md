
# Server
The server for Twitch Market handles the connection to Twitch and directs messages to the clients. It has basic command management for commands received from the clients.
___

**send_message**(*socketobj, message*)

This is the main method of communication between clients and the main server. It turns a message (usually json) into bytes and sends it across a socket.

**recv_message**(*socketobj*)

Receives bytes from the socket and decodes them.

**accept\_connections**(*server\_socket, worker\_queue*)

Run as a process. Accepts all incoming connections to the server and closes ones that are not on the local network.

**connection\_handle**(*work\_queue, worker\_queue, whisper\_queue, connection*)


Sends a message out to a connection to be parsed then receives the response from the client and parses it. 

Possible responses:

<table style="border: 1px solid black;">
	<tr>
		<th>Key word</th>
		<th>Description</th>
	</tr>
	<tr>
		<td>Send</td>
		<td>A client requests to send a message to twitch. Message is added to queue. Message format: (username, message)</td>
	</tr>
		<td>End</td>
		<td>A client passes then is not added back into the worker_queue.</td>
	<tr>
		<td>Pass</td>
		<td>A client passes.</td>
	</tr>
</table>

**handout_work**(*whisper\_queue*)

Gives work out to clients that are in the worker_queue. Spawns a connection_handle for each message that is sent to each client.

**recieve\_from\_twitch**(*work\_queue, twitch\_socket*)

Receives whisper from Twitch then places them into the work_queue.



**send_whispers**(*whisper\_queue, twitch\_socket*)

Sends whispers in the whisper queue to twitch.
