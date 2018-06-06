# appreciate_blockchain

Requirements:

Python 3.6.x

Postman or curl

Python dependencies:

Flask: pip install flask==0.12.2;

requests: pip install requests==2.18.4;

hshlib: pip intsall hashlib;

json: pip install json;

uuid: pip install uuid(maybe present);


General instructions:

Clone the repository and map the path on command line to where Block/ folder is stored.

Run python script: python blockchain.py;

Open postman and register nodes: http://localhost:500x/nodes/register using POST request.

In json body enter: "nodes":["http://127.0.0.1:500x"]

Open home.html on any browser.
