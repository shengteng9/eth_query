# coding=utf-8
from flask import Flask, render_template, request, jsonify

from web3 import Web3, HTTPProvider

# 新建一个Flask应用
app = Flask(__name__)

# 初始化web3
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/e8ee044513804b0791a9b53f0a63d742"))


@app.route("/")
def get_lask_block():
    # 获取最新区块
    last_block = w3.eth.getBlock('latest')

    # 提取区块信息
    block = {
        "miner": last_block.miner,
        "difficulty": last_block.difficulty,
        "extraData": last_block.extraData.hex(),
        "gasLimit": last_block.gasLimit,
        "gasUsed": last_block.gasUsed,
        "hash": last_block.hash.hex(),
        "logsBloom": last_block.logsBloom.hex(),
        "mixHash": last_block.mixHash.hex(),
        "nonce": last_block.nonce.hex(),
        "number": last_block.number,
        "parentHash": last_block.parentHash.hex(),
        "receiptsRoot": last_block.receiptsRoot.hex(),
        "size": last_block.size,
        "stateRoot": last_block.stateRoot.hex(),
        "timestamp": last_block.timestamp,
        "totalDifficulty": last_block.totalDifficulty,
        "transactionsRoot": last_block.transactionsRoot.hex(),
        "transactions": [],
        "uncles": last_block.uncles,
    }

    for t in last_block.transactions:
        block['transactions'].append(
            t.hex()
        )
    return render_template("block.html", block=block)


@app.route("/transaction", methods=["GET", "POST"])
def handle_transaction():
    if request.method == 'GET':
        return render_template("transaction.html")
    else:
        h = request.form.get("transaction")
        transaction = w3.eth.getTransaction(h)
        result = {
            "blockHash": transaction.blockHash.hex(),
            "blockNumber": transaction.blockNumber,
            "from": transaction["from"],
            "gas": transaction.gasPrice,
            "gasPrice": transaction.gasPrice,
            "hash": transaction.hash.hex(),
            "input": transaction.input,
            "nonce": transaction.nonce,
            "r": transaction.r.hex(),
            "s": transaction.s.hex(),
            "to": transaction.to,
            "transactionIndex": transaction.transactionIndex,
            "v": transaction.v,
            "value": transaction.value
        }
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
