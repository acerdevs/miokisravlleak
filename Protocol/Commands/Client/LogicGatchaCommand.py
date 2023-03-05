from ByteStream.Reader import Reader
from Utils.Helpers import Helpers
from Logic.Home.LogicShopData import LogicShopData
import random
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage

class LogicGatchaCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()
        self.box_id = self.readVInt()


    def process(self, db):

        self.player.delivery_items = {
            'Count': 1,
            'Type': 0,
            'Items': []
        }

        item = {'Amount': 85, 'DataRef': [0, 0], 'SkinRef': [0, 0 ], 'Value':7 }
        self.player.delivery_items['Type'] = 100
        self.player.delivery_items['Items'].append(item)
        self.player.resources[1]['Amount'] = self.player.resources[1]['Amount'] + 95
        db.update_player_account(self.player.token, 'Resources', self.player.resources)



        self.player.db = db
        AvailableServerCommandMessage(self.client, self.player, 203, {}).send()



