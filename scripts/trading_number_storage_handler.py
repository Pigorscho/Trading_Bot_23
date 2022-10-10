class TradingNumberStorage:
    def __init__(self):
        self.total_min_profit = 0
        self.sell_price = 0
        self.tl_amount = 0
        self.tl_selling = 0
        self.tl_sold = 0
        self.bank_account = 0
        self.succ_purchase = 0

    # def get_total_min_profit(self): return self.total_min_profit
    def add_min_profit(self, min_profit_to_add): self.total_min_profit += min_profit_to_add
    # def get_sell_price(self): return self.sell_price
    # def add_sell_price(self, sell_price_to_add): sell_price_to_add -= self.sell_price
    # def get_transfer_list_amount(self): return self.tl_amount
    def add_transfer_list_amount(self, tl_amount_to_add): self.tl_amount += tl_amount_to_add
    # def get_transfer_list_selling(self): return self.tl_selling
    def add_transfer_list_selling(self, tl_selling_to_add): self.tl_selling += tl_selling_to_add
    # def get_transfer_list_sold(self): return self.tl_sold
    def add_transfer_list_sold(self, tl_sold_to_add): self.tl_sold += tl_sold_to_add
    # def get_bank_account(self): return self.bank_account
    def set_bank_account(self, current_bank_account): self.bank_account = current_bank_account
    def set_succ_purchase(self, succ_purchase_to_add): self.succ_purchase = succ_purchase_to_add
    def increment_succ_purchase(self): self.succ_purchase += 1
    def to_dict(self): return self.__dict__


if __name__ == '__main__':
    profit_handle = TradingNumberStorage()
    profit_handle.add_min_profit(42)
    profit_handle.add_min_profit(42)
    profit_handle.add_transfer_list_sold(42)
    profit_handle.add_transfer_list_amount(42)
    profit_handle.add_transfer_list_selling(42)
    profit_handle.tl_sold += 42
    print(profit_handle.to_dict())
