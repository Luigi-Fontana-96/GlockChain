import requests
from datetime import datetime
from pprint import pprint

class Bitcoin_interactor:

    def __init__(self):
        self.tx_json = {} # json of the entire request
        self.tx_info = {} # transantion info
        self.utxo_inputs = {} # Input UTXO
        self.utxo_outputs = {} # Output UTXO
        
    # Method that request Tx info
    def bitcoin_transaction_DataRetrieval(self,hash):
        url = f'https://api.blockchair.com/bitcoin/dashboards/transaction/{hash}'
        response = requests.get(url)
        if response.status_code == 200:
            self.tx_json = response.json()   
            self.UTXO_extractor(hash)
        else:
            print(f"Request failed with status code {response.status_code}, please controll the hash")
                
    # Method to extract the TX info  
    def UTXO_extractor(self,hash):       
        data = self.tx_json['data'] 
        tx = data[hash] # Selecting the right keys

        self.tx_info = tx["transaction"] # The info of the tx
        self.utxo_inputs  = tx['inputs'] # The input Utxo
        self.utxo_outputs = tx['outputs'] # The output Utxo       