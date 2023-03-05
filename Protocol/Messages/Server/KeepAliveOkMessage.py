from ByteStream.Writer import Writer
from DataBase.MongoDB import MongoDB
from datetime import datetime
import random
from Protocol.Messages.Server.LoginFailedMessage import LoginFailedMessage

class KeepAliveOkMessage(Writer):

    def __init__(self, client, player, db: MongoDB):
        super().__init__(client)
        self.id = 20108
        self.player = player
        self.db = db

    def encode(self):
        pass

