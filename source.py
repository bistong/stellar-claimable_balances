from stellar_sdk import Server, Keypair, TransactionBuilder, Network
import requests
import json         

######
###### stellar claimable_balances
###### akan otomatis add asset jika belum ada, pastikan stok XLM masih cukup 
###### script ini hanya mentah saja, silahkan disempurnakan
###### Donasi XLM GBOOIATLLIPVV5P55HKK5IIFJ5QSKB2EKNVSHFW4XAO64TEGZMVUXOER
###### secretkey simpan di "sk.txt" dengan format 1 SK 1 baris (baris 56)
###### jangan lupa install stellar-sdk (pip install stellar-sdk)
######
###### source by https://t.me/xoerbiston


def exe(SK):
	server = Server(horizon_url="https://horizon.stellar.org")
	root_keypair = Keypair.from_secret(SK)
	root_account = server.load_account(account_id=root_keypair.public_key)
	public_key = root_keypair.public_key
	peka = public_key[0:10]+"..."+public_key[len(public_key)-10:]

	url = 'https://horizon.stellar.org/claimable_balances?limit=1&claimant='+public_key
	body = {}
	r = requests.get(url, data=json.dumps(body))
	if len(r.json()['_embedded']['records']) != 0 :
		balance_id = r.json()['_embedded']['records'][0]['id']
		jum        = r.json()['_embedded']['records'][0]['amount']
		aset0      = r.json()['_embedded']['records'][0]['asset']
		aset1 = aset0.split(":")
		aset = aset1[0]
		issuer = aset1[1]
		try:
			tgl0 = r.json()['_embedded']['records'][0]['claimants'][0]['predicate']['and'][0]['not']['abs_before']
		except:
			tgl0 = r.json()['_embedded']['records'][0]['claimants'][0]['predicate']['not']['abs_before']
		tgl = tgl0.split("T")
		print("=> "+peka+" : "+aset+" "+jum+" "+tgl[0])
	else :
		print("=> "+peka+" : null")
		exit()

	transaction = (
		TransactionBuilder(
			source_account=root_account,
			network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
			base_fee=100,
		)
		.append_change_trust_op(aset,issuer,limit=None,source=None)
		.append_claim_claimable_balance_op(balance_id=balance_id,source=None)
		.set_timeout(30)
		.build()
		)
	transaction.sign(root_keypair)
	response = server.submit_transaction(transaction)

with open('sk.txt') as my_file:
	for line in my_file:
		try:
			bis = str(line.strip())
			if (bis[0:1]=="S"):
				exe(bis)
		except Exception as e:
				y = json.loads(str(e))
				ton = "   "+y['title']
				print(ton)
		except:
			pass

print("")
print("### SELESAI...###")
