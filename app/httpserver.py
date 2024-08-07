from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS from Flask-CORS
from config import *
from database import *
from rpc import block_bits2target,rpc_getwallet,rpc_gettxn
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the Flask app
database=Database()


# API endpoint to get the data
def MinertoJson(obj):
    t={"user_id":obj.user_id,"username":obj.username,"target":str(obj.target),"hashrate":obj.hashrate}
    return t
def toJsonShareData(data):
    target=block_bits2target(data.target_network)
    return {"id":data.share_id,"share":data.difficulty,"target":str(target.hex()),"datetime":data.datetime}
@app.route('/users/<int:user_id>', methods=['GET'])
def get_data(user_id):
    user_data=database.find_one(Miner,user_id=user_id)
    # if user_data:    
    #     data_shares=database.find_all(ShareRecord,user_id=user_id)
    #     data_list = [toJsonShareData(record) for record in data_shares]
    if not user_data:
        return jsonify({"data":{} })
        

    return jsonify({"data":MinertoJson(user_data) })
@app.route('/users/data', methods=['GET'])
def get_pool_data():
    response=[]
    # user_data=database.custom_query("select * from miners,share_record where miners.id=share_record.id_user")
    users=database.find_all(Miner)
    if not users:
        users=[]
    tt_hashrate=0
    walletinfo=rpc_getwallet()
    total=0
    json_users=[]
    for user in users:
        json_users.append(MinertoJson(user))
        if user.hashrate is not None:
            tt_hashrate+=int(str(user.hashrate))
    rewards=database.find_all(Reward)
    if rewards:
        for reward in rewards:
            t=rpc_gettxn(reward.reward_id,reward.block)
            total+=t["vout"][0]["value"]
    else:
        rewards=[]
    
    pool_data=({"title":"Pool Information",
    "numberMiners": len(users),
    "miners":json_users,
    "total_hashrate": tt_hashrate,
    "balance":walletinfo["balance"],
    "immature_balance":walletinfo["immature_balance"],
    "unconfirmed_balance":walletinfo["unconfirmed_balance"],
    "unit":"BTC",
    "block_mined":len(rewards),
    "reward":total}
    )
    response.append(pool_data)
    return jsonify({"data":response })


if __name__ == '__main__':
    app.run(debug=True, host=HTTP_SERVER, port=int(HTTP_PORT))
