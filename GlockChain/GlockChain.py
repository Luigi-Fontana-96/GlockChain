from Neo4j_connector import Neo4j_connector
from Bitcoin_interactor import Bitcoin_interactor
import os
import ast
from os.path import join, dirname
from dotenv import load_dotenv

# ambient settings
dotenv_path = join(dirname(__file__), '.env') 
load_dotenv(dotenv_path)
# credentials settings
auth = ast.literal_eval(os.environ.get('AUTH')) 
url = os.environ.get('URL')

title = """
 +--^----------,--------,-----,--------^-,
 | |||||||||   `--------'     |          O
 `+---------------------------^----------|
   `\_,---------,---------,--------------'  __   _________  __            __ 
    / xxxxxx / /  _____/|  |   ____   ____ |  | _\_   ___ \|  |__ _____  |__| ____  
   / xxxxxx / /   \  ___|  |  /  _ \_/ ___\|  |/ /    \  \/|  |  \\__  \ |  |/    \ 
  / xxxxxx /  \    \_\  \  |_(  <_> )  \___|    <\     \___|   Y \/ __ \|  |   |  \\
 / xxxxxx /    \______  /____/\____/ \___  >__|_ \\______  /___|  (____  /__|___|  /
(________/            \/                 \/     \/       \/     \/     \/        \/  
 
"""

def display_menu():
    print("Authors: Luigi Fontana")
    print("Linkedin: https://www.linkedin.com/in/luigi-fontana-396479279/")
    print("GitHub: https://github.com/Luigi-Fontana-96")
    print(title)
    print("+++++++++++++++++++++++")
    print("What you want to do?")
    print("1. Store in the Database")
    print("2. Delete from the Database")
    print("3. Exit")

def store_Database():
    interactor = Bitcoin_interactor()
    connector = Neo4j_connector(url,auth)
    while True:
        print("-----------------------")
        print("What you want to store?")
        print("1. Store Transaction")
        print("2. Exit")
        try:
            choice = int(input("Choice your action-> "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
                   
        if choice == 1:
            print("Insert the TXs to store (hash comma separated)")
            hash = input("-->")
            hash_list = hash.split(',')
            for item in hash_list: 
                interactor.bitcoin_transaction_DataRetrieval(item) # The object interactor contains 3 dictionary that contains the info about the TX and the UTXO
                connector.store_transaction_Info(interactor) # Here the funcion create the nodes and the relactions of the UTXO and the TX
        elif choice == 2:
            print("Exiting store functionalities.")
            print("-----------------------")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 2.")

def delete_Database():
    connector = Neo4j_connector(url,auth)
    while True:
        print("-----------------------")
        print("What you want to Delete?")
        print("1. Delete Transaction")
        print("2. Delete Transaction and associated UTXO")
        print("3. Delete UTXO")
        print("4. Exit")
        try:
            choice = int(input("Choice your action-> "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
                   
        if choice == 1:
            hash_list = input("\nInsert the TX you want to delete (hash comma separated) -->")
            hash = hash_list.split(',')
            for h in hash:
                connector.delete_transaction_Info(h)
        if choice == 2:
            hash_list = input("\nInsert the TX you want to delete (hash comma separated) -->")
            hash = hash_list.split(',')
            for h in hash:
                connector.delete_transaction_and_UTXO_Info(h)
        elif choice == 3:
            utxo_list = input("\nInsert the UTXO you want to delete (hash comma separated) -->")
            utxo = utxo_list.split(',')
            for u in utxo:
                connector.delete_utxo_Info(u)
            break
        elif choice == 4:
            print("Exiting store functionalities.")
            print("-----------------------")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def main():
    while True:
        display_menu()

        try:
            choice = int(input("Choice your action-> "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            store_Database()
        elif choice == 2:
            delete_Database()
        elif choice == 3:
            print("Exiting the Glock Chain. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    print("\nWelcome to GlockChain a Bitcon chain Analyzer Tool\n")
    main()
