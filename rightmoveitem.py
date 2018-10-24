class RightMoveItem:

#    id = ""
#    desc = ""
#    address = ""
#    price = ""
#    data = ""
#    reduced = ""
 #   agent = ""
#    ls = [id, desc, address, price, data, reduced, agent]

    def __init__(self, id, desc, address, price, date, reduced, agent):
        self._id = id
        self._desc = desc
        self._address = address
        self._price = price
        self._date = date
        self._reduced = reduced
        self._agent = agent

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.ls)

    @property
    def id(self):
        if self._id:
            return self._id
        else:
            return "Unknown"

    @property
    def desc(self):
        if self._desc:
            return self._desc
        else:
            return "Unknown"

    @property
    def address(self):
        if self._address:
            return self._address
        else:
            return "Unknown"

    @property
    def price(self):
        if self._price:
            return self._price
        else:
            return "Unknown"

    @property
    def date(self):
        if self._date:
            return self._date
        else:
            return "Unknown"

    @property
    def reduced(self):
        if self._reduced:
            return self._reduced
        else:
            return "Unknown"

    @property
    def agent(self):
        if self._agent:
            return self._agent
        else:
            return "Unknown"

    def to_array(self):
        return [self.id, self.desc, self.address, self.price, self.date, self.reduced, self.agent]

    def to_string(self):
        ret = ("id: " + str(self.id) + ", desc: " + self.desc + ", address: " + self.address + ", price: " + self.price + ", date: " + self.date + ", agent: " + self.agent)
        return ret