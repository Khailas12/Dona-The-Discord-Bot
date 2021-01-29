from flask import Flask
from threading import Thread

dona = Flask("")

@dona.route('/')
def home():
	return "Dona is Alive!"

def run():
	dona.run(host='0.0.0.0', port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()
	
