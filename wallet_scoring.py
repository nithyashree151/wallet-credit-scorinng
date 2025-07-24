import json
import pandas as pd

with open('data/user_transactions.json') as f:
    data = json.load(f)

wallets = {}

for tx in data:
    wallet = tx['wallet_address']
    action = tx['action']
    amount = float(tx['amount'])
    if wallet not in wallets:
        wallets[wallet] = {'score': 500}
    if action == 'deposit':
        wallets[wallet]['score'] += amount * 0.2
    elif action == 'repay':
        wallets[wallet]['score'] += amount * 0.1
    elif action == 'borrow':
        wallets[wallet]['score'] -= amount * 0.15
    elif action == 'liquidationcall':
        wallets[wallet]['score'] -= amount * 0.3
    elif action == 'redeemunderlying':
        wallets[wallet]['score'] += amount * 0.05

for wallet in wallets:
    wallets[wallet]['score'] = min(1000, max(0, round(wallets[wallet]['score'])))

df = pd.DataFrame([
    {'wallet_address': w, 'score': wallets[w]['score']}
    for w in wallets
])
df.to_csv('output/wallet_scores.csv', index=False)
