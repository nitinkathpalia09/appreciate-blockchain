import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import socket
import operator
from bs4 import BeautifulSoup
import itertools
import requests
from flask import Flask, jsonify, request, redirect, url_for,render_template


class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)
        self.points=0
    
    def register_node(self, address):


        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
            
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
    
            

    def new_block(self, proof, previous_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def counter(self):
        count=0
        points=0
        count=len(self.current_transactions)
        points=count*2
        self.points=points
        return count,points

        
    
    def position(self):
        neighbour=self.nodes
        list=[]
        nodes_other=[]
        points_final=[]
        #nodes_list=[]
        #my_dict={}
        points_self=self.points
        for node in neighbour:
            response= requests.get(f'http://{node}/counter').text
            soup=BeautifulSoup(response,'html.parser')
            abc=soup.find_all('td')
            for link in abc:
                values=link.contents[0]
                list.append(values)
            points_final.append(int(list[1]))
            nodes_other.append(list[2])
                #dcf=list[1]
            #nodes_other.append(dcf)
            

                #nodes_list.append(node)
                #my_dict.update({'node':points_final[node]})

        points_final.append(points_self) 
        nodes_other.append(socket.gethostname())
        Z = [x for _,x in sorted(zip(points_final,nodes_other),reverse=True)]
        Y=sorted(points_final,reverse=True)
        #for node in neighbour:
         #   self.dict.update({'node':points_final[node]})       
        #sorted_dict=sorted(self.dict.items(),key=operator.itemgetter(1))
                
        #return sorted_dict
        return Y,Z
    def transactions(self, sender, recipient,address):
           
        self.current_transactions.append({
            'sender': socket.gethostname(),
            'recipient': recipient,
            'address': address,
        
            
        })
    
        return self.last_block['index'] + 1
        
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
    

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):


        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    

# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.transactions(
        sender="0",
        recipient=node_identifier,
        address="0",
        
        
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
@app.route('/counter',methods=['GET'])
def counter():
    count,points=blockchain.counter()
    response={
        'Appreciate Count':count,
        'Appreciate Points':points,
        'Node':socket.gethostname()
    }
    return render_template('counter2.html', result=response)
   
    #return jsonify(response), 200
@app.route('/success/<name>')
def success(name):
    return 'successfully appreciated the employee for the month  %s' %name
@app.route('/transactions', methods=['POST','GET'])
def transactions():
    if request.method=='POST':
        recipient = request.form['recipient']
        address=request.form['url']
        
    
        index = blockchain.transactions(socket.gethostname(), recipient,address)
        return redirect(url_for('success',name=index))
   
    

    else:
        recipient=request.args.get('recipient')
        address=request.args.get('url')
       
        index = blockchain.transactions(socket.gethostname(),recipient,address)
        
        return redirect(url_for('success',name=index))




@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200




@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
@app.route('/position',methods=['GET'])
def position():
    points,nodes=blockchain.position()
    
    response={
        'points': points,
        'nodes': nodes
        
    }
    return render_template('position2.html', result=response)
    

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=5001)