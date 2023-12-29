import requests
from web3.auto import w3
import sys
import os
import urllib.parse
from eth_account import Account
import json

# Enable the unaudited HD wallet features
Account.enable_unaudited_hdwallet_features()

# Get the 12 words from command line arguments
words = sys.argv[1:]

# Join the words with %20 separator to form the URL
url = "https://nft.poczta-polska.pl/wallet?m=" + "%20".join(words)
url2 = "https://nft.poczta-polska.pl/wallet?m=" + urllib.parse.quote(" ".join(words))
# print link
# czasem jeden sposób nie działa dlatego dajemy dwa
print(" --- *** --- ")
print("Link:", url)
print("Link2:", url2)
print(" ")

# Generate private key and wallet address catch error if words are wrong
try:
    private_key = w3.eth.account.from_mnemonic(" ".join(words))._private_key.hex()
    wallet_address = w3.eth.account.from_mnemonic(" ".join(words)).address
except:
    print("Wrong words!")
    sys.exit()

# private_key = w3.eth.account.from_mnemonic(" ".join(words))._private_key.hex()
# wallet_address = w3.eth.account.from_mnemonic(" ".join(words)).address

# Check balance of wallet address using polygonscan API
api_key = "TWOJ_API_KEY"
# Adres kontraktu NFT, który chcesz sprawdzić
nft_contract_address = "0x753b3B27b4D3ff63957297313469b84fCec98b3c"  # janek - nie jest to konieczne
balance_url = f"https://api.polygonscan.com/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={api_key}"
response = requests.get(balance_url)
balance = int(response.json()["result"]) / 10**18


# checkt NFT balance using polygonscan API
nft_url = f"https://api.polygonscan.com/api?module=account&action=token1155tx&address={wallet_address}&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey={api_key}"
response = requests.get(nft_url)
nft = response.json()["result"]

#ponizsze fragmenty zakomentowane ze wzgledu na szybkosc dzialania

# #check tranfers to wallet address using polygonscan API
# tranfers_url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}"
# response = requests.get(tranfers_url)
# tranfers = response.json()["result"]

# check NFT transfers to wallet using polygonscan API
# nft_tranfers_url = f"https://api.polygonscan.com/api?module=account&action=tokennfttx&address={wallet_address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}"
# response = requests.get(nft_tranfers_url)
# nft_tranfers = response.json()["result"]

# generate polygonscann wallet adress for erc1155 tokens
# https://polygonscan.com/address/0xb8152ed2163b4dbbbc0daf3a1d269ea1d6ee10ee#tokentxnsErc1155
polygonscan_url = f"https://polygonscan.com/address/{wallet_address}#tokentxnsErc1155"

# Print private key, wallet address, and balance
print(" --- *** --- ")
print("Private Key:", private_key)
print("Wallet Address:", wallet_address)
print("Polygonscan:", polygonscan_url)
print("Balance:", balance)
print("NFT:", json.dumps(nft, indent=4, sort_keys=True))
##print transfers with pretty print json data
##print("Tranfers:", json.dumps(tranfers, indent=4, sort_keys=True))
##print("NFT Tranfers:", json.dumps(nft_tranfers, indent=4, sort_keys=True))

# if nft != [] wywołaj polecenie systemowe say "masz nft"
# działa na maku i powinno na linuxach - inne systemy niekoniecznie
# if nft != []:
#     print("Masz NFT!")
#     os.system("say Masz NFT!")


