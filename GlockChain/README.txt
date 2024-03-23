Strumento di analisi Blockchain Bitcoin sviluppato per la tesi di laurea magistrale in Ingegneria Informatica presso l'università degli studi di Catania.

Guida allo start-up dell'applicativo:

Il software è formato da due componenti:
- Glockchain
- Neo4J

Il primo passo è scaricare Neo4j Desktop.
L'applicativo è stato testato su Neo4j versione 1.5.9

Il secondo passo è creare un ambiente virtuale python, la versione testata è la 3.8.10, e scaricare
le librerie necessarie lanciando il file requirements.txt col comando: pip install -r requirements.txt

Il terzo passo è creare un nuovo database su Neo4j e inserire le credenziali di accesso sul file .env

Avviare l'applicativo dal file GlockChain.py e seguire il menù interattivo.
Aggiunte o rimosse le informazioni, le stesse saranno visibili su Neo4j Browser con la query: Match (n) return n.
