from database import Database,Miner
database=Database()
database.create_all_entities(drop_existing=True)
miner = Miner(user_id='123', username='username', password='password', address='bcrt1qgwev460zqprwlvnv45nq3tyuwgj4t8ukx8qs53',hashrate=0,target="0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
miner1 = Miner(user_id='1234', username='username1', password='password', address='bcrt1qgwev460zqprwlvnv45nq3tyuwgj4t8ukx8qs53',hashrate=0,target="0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
database.add_data(miner)
database.add_data(miner1)
