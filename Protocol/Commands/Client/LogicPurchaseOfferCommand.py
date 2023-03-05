from ByteStream.Reader import Reader
from Logic.Home.LogicShopData import LogicShopData
import random
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage

class LogicPurchaseOfferCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()

        self.offer_index = self.readVInt()

        self.brawler = self.readDataReference()[1]

    def process(self, db):
        offer_claim       = LogicShopData.offers[self.offer_index]['ClaimID']
        if offer_claim in self.player.claimshop:
            offer_claim_b = True
        else:
            offer_claim_b = False
        offer_count       = LogicShopData.offers[self.offer_index]['OffersCount']
        offer_resource = LogicShopData.offers[self.offer_index]['ShopType']
        offer_cost     = LogicShopData.offers[self.offer_index]['Cost']
        if offer_count >= 1:
            offer_id       = LogicShopData.offers[self.offer_index]['OfferID']
            offer_amount   = LogicShopData.offers[self.offer_index]['Multiplier']
            offer_skin   = LogicShopData.offers[self.offer_index]['SkinID']
            offer_char = LogicShopData.offers[self.offer_index]['DataReference'][1]
        if offer_count >= 2:
            offer_id2       = LogicShopData.offers[self.offer_index]['OfferID2']
            offer_amount2   = LogicShopData.offers[self.offer_index]['Multiplier2']
            offer_skin2   = LogicShopData.offers[self.offer_index]['SkinID2']
            offer_char2 = LogicShopData.offers[self.offer_index]['DataReference2'][1]
        if offer_count >= 3:
            offer_id3       = LogicShopData.offers[self.offer_index]['OfferID3']
            offer_amount3   = LogicShopData.offers[self.offer_index]['Multiplier3']
            offer_skin3   = LogicShopData.offers[self.offer_index]['SkinID3']
            offer_char3 = LogicShopData.offers[self.offer_index]['DataReference3'][1]

        if True:
            item = {'Amount': offer_amount, 'DataRef': [0, 0], 'SkinRef': [0, 0 ], 'Value':7 }
            self.player.delivery_items['Type'] = 100
            self.player.delivery_items['Items'].append(item)
            self.player.resources[1]['Amount'] = self.player.resources[1]['Amount'] + offer_amount
            db.update_player_account(self.player.token, 'Resources', self.player.resources)

        if not offer_claim_b:
            if offer_claim != "starrroad_rare" and offer_claim != "starrroad_superrare" and offer_claim != "starrroad_epic" and offer_claim != "starrroad_megaepic" and offer_claim != "starrroad_legendary" and offer_claim != "898989":
                self.player.claimshop.append(offer_claim)
                db.update_player_account(self.player.token, 'ClaimShop', self.player.claimshop)

            if offer_resource == 0:
                self.player.gems = self.player.gems - offer_cost
                db.update_player_account(self.player.token, 'Gems', self.player.gems)

            elif offer_resource == 1:
                self.player.resources[1]['Amount'] = self.player.resources[1]['Amount'] - offer_cost
                db.update_player_account(self.player.token, 'Resources', self.player.resources)

            elif offer_resource == 3:
                self.player.resources[3]['Amount'] = self.player.resources[3]['Amount'] - offer_cost
                db.update_player_account(self.player.token, 'Resources', self.player.resources)

            self.player.db = db

            AvailableServerCommandMessage(self.client, self.player, 203, {}).send()



