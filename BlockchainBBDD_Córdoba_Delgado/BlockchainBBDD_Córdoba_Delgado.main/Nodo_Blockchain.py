from hashlib import sha256
import json
import time
import socket
import pickle
import os
from threading import Thread

puerto = 8000

class BlocK:
    def __init__(self,id, hash_previo, datos, nonce = 0):
        self.id = id
        self.hash_previo = hash_previo
        self.datos = datos
        self.nonce = nonce
        self.hash = self.CalcularHash()
    def CalcularHash(self): 
        data = str(self.hash_previo).encode()+str(self.id).encode()+str(self.datos).encode()+str(self.nonce).encode()
        h = sha256()
        h.update(data)
        return h.hexdigest()
    
class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self, chain=None):
        self.chain = chain
        if self.chain is None:
            self.chain = []
            self.crear_bloque_alfa()

    def crear_bloque_alfa(self):
        bloque_alfa = BlocK(0,0,"")
        self.chain.append(bloque_alfa)
    
    def ultimo_bloque(self):
        return self.chain[-1]
    
    def PoW(self,block):
        block.nonce = 0
        computed_hash = block.CalcularHash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.CalcularHash()

        return computed_hash


    def mine(self, datos):
        last_block = self.ultimo_bloque()
        new_block = BlocK(last_block.id + 1, last_block.hash, datos)
        proof = self.PoW(new_block)
        new_block.hash = proof
        self.chain.append(new_block)  
        return True
    

class Nodo_Blockchain:
    def __init__(self, copia_blockchain):
        self.copia_blockchain = copia_blockchain
        self.blockchain_file = "blockchain.p"

    def mostrar_copia_blockchain(self):
        for bloque in self.copia_blockchain.chain:
            if bloque.id == 0:
                print("Bloque Alfa")
            print("El bloque "+str(bloque.id)+" contiene:"+str(bloque.datos)+" Hash "+str(bloque.hash))

    def guardar_blockchain(self):
        with open(self.blockchain_file, 'wb') as f:
            pickle.dump(self.copia_blockchain, f)

    def cargar_blockchain(self):
        if os.path.exists(self.blockchain_file):
            with open(self.blockchain_file, 'rb') as f:
                self.copia_blockchain = pickle.load(f)
    
    
if __name__ == "__main__":
    blockchain = Blockchain()
    nodo = Nodo_Blockchain(blockchain)
    nodo.cargar_blockchain()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', puerto))
    sock.listen()

    while True:
        try:
            conn, address = sock.accept()
            data = conn.recv(1024)
            if data:
                nodo.copia_blockchain.mine(data.decode())
                nodo.mostrar_copia_blockchain()
                print("************************************************************************************************")
                print("************************************************************************************************")
            conn.close()
            time.sleep(3)
        except KeyboardInterrupt:
            print("Deteniendo el servidor...")
            break
        finally:
            nodo.guardar_blockchain()
            print("Blockchain guardada.")