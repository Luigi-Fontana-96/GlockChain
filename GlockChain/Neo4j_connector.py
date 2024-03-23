from neo4j import GraphDatabase

class Neo4j_connector:
    
    def __init__(self,url,auth):
        self.url = url
        self.auth = auth
    
    #Method to store the info of a transaction
    def store_transaction_Info(self, interactor):
        try:
            with GraphDatabase.driver(self.url, auth=self.auth) as driver:
                driver.verify_connectivity()
                print("Processing storage:")
                self.create_TX(driver, interactor.tx_info)
                self.create_input_UTXO(driver, interactor.utxo_inputs)
                self.create_output_UTXO(driver, interactor.utxo_outputs)
                
                print("Storage Complete")
        except Exception as e:
            print(f"The method store_transaction_Info has launched an Exception: {e}")

    #Method to create a transaction node
    def create_TX(self,driver,tx_info):
        summary = driver.execute_query(
        """
        MERGE (:Transaction {
            name: $name,
            time: $time,
            block_id: $block_id,
            coinbase: $coinbase,
            input_count: $input_count,
            output_count: $output_count,
            input_value: $input_value,
            input_value_usd: $input_value_usd,
            output_value: $output_value,
            output_value_usd: $output_value_usd
        })
        """,
        name =tx_info['hash'],
        time=tx_info['time'],
        block_id=tx_info['block_id'],
        coinbase=tx_info['is_coinbase'],
        input_count=tx_info['input_count'],
        output_count=tx_info['output_count'],
        input_value=tx_info['input_total'],
        input_value_usd=tx_info['input_total_usd'],
        output_value=tx_info['output_total'],
        output_value_usd=tx_info['output_total_usd']
    ).summary
        print("TX--> {}" .format(tx_info['hash']))

    #Method to create an UTXO node from the input of the TX
    def create_input_UTXO(self,driver,utxo_inputs):
        
        for item in utxo_inputs:
            summary = driver.execute_query(
            """
            MERGE (:UTXO {
                name: $name,
                time: $time,
                block_id: $block_id,
                recipient: $recipient,
                value: $value,
                value_usd: $value_usd,
                is_spent: $is_spent,
                spending_transaction_hash: $spending_transaction_hash
            })
            """,
            name =item['transaction_hash'] +":"+ str(item['index']),
            time=item['time'],
            block_id=item['block_id'],
            recipient=item['recipient'],
            value=item['value'],
            value_usd=item['value_usd'],
            is_spent=item['is_spent'],
            spending_transaction_hash=f"{item['spending_transaction_hash']}"

        ).summary
            print("UTXO--> {}:{}" .format(item['transaction_hash'], item['index']))
            
            self.create_input_Relation(driver, item['transaction_hash'] +":"+ str(item['index']), item['spending_transaction_hash'])
             
    #Method to create an UTXO node from the output of the TX
    def create_output_UTXO(self,driver,utxo_outputs):
        
        for item in utxo_outputs:
            summary = driver.execute_query(
            """
            MERGE (:UTXO {
                name: $name,
                time: $time,
                block_id: $block_id,
                recipient: $recipient,
                value: $value,
                value_usd: $value_usd,
                is_spent: $is_spent,
                spending_transaction_hash: $spending_transaction_hash
            })
            """,
            name =item['transaction_hash'] +":"+ str(item['index']) ,
            time=item['time'],
            block_id=item['block_id'],
            recipient=item['recipient'],
            value=item['value'],
            value_usd=item['value_usd'],
            is_spent=item['is_spent'],
            spending_transaction_hash=f"{item['spending_transaction_hash']}"
        ).summary
            print("UTXO--> {}:{}" .format(item['transaction_hash'], item['index']))
            
            self.create_output_Relation(driver, item['transaction_hash'] +":"+ str(item['index']), item['transaction_hash'])
        
    def create_input_Relation(self,driver,utxo_id,tx_id):
        records, summary, keys = driver.execute_query(
        f"""
            MATCH (u:UTXO) WHERE u.name='{utxo_id}' 
            MATCH (t:Transaction) WHERE t.name='{tx_id}' 
            MERGE (u)-[:INPUT]->(t)
        """
        )

    def create_output_Relation(self,driver,utxo_id,tx_id):
        records, summary, keys = driver.execute_query(
        f"""
        MATCH (t:Transaction) WHERE t.name='{tx_id}'
        MATCH(u:UTXO) WHERE u.name='{utxo_id}' 
        MERGE (t)-[:OUTPUT]->(u)
        """
        )
   
    def delete_transaction_Info(self, hash):
        try:
            with GraphDatabase.driver(self.url, auth=self.auth) as driver:
                driver.verify_connectivity()
                print("Processing delete:")
                records, summary, keys = driver.execute_query(
                f"""
                MATCH (t:Transaction) WHERE t.name='{hash}'
                DETACH DELETE t
                """
                )
                print("Deleting TX --> {}" .format(hash))
                print("Delete Complete")
        except Exception as e:
            print(f"The method delete_transaction_Info has launched an Exception: {e}")
    
    def delete_transaction_and_UTXO_Info(self, hash):
        try:
            with GraphDatabase.driver(self.url, auth=self.auth) as driver:
                driver.verify_connectivity()
                print("Processing delete:")
                records, summary, keys = driver.execute_query(
                f"""
                Match (t:Transaction) where t.name='{hash}'
                Match (u:UTXO) where (u)-[:INPUT]->(t) or (t)-[:OUTPUT]->(u)
                Detach Delete u,t;
                """
                )
                print("Deleting TX --> {}" .format(hash))
                print("Delete Complete")
        except Exception as e:
            print(f"The method delete_transaction_Info has launched an Exception: {e}")
    
    def delete_utxo_Info(self, utxo):
        try:
            with GraphDatabase.driver(self.url, auth=self.auth) as driver:
                driver.verify_connectivity()
                print("Processing delete:")
                records, summary, keys = driver.execute_query(
                f"""
                MATCH (u:UTXO) WHERE u.name='{utxo}'
                DETACH DELETE u
                """
                )
                print("Deleting UTXO --> {}" .format(utxo))
                print("Delete Complete")
        except Exception as e:
            print(f"The method delete_utxo_Info has launched an Exception: {e}")