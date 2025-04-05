import json

class MenuItem:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        self.items = [item for item in self.items if item.id != item_id]

    def get_items(self):
        return self.items

    def to_json(self):
        
        pass

    @classmethod
    def from_json(cls, json_data):
        cart = cls()
        if json_data:
            try:
                cart_data = json.loads(json_data)

                for item_data in cart_data:
                    item = MenuItem(item_data['id'], item_data['name'], item_data['price'])
                    cart.add_item(item)
            except json.JSONDecodeError:
                pass  
        return cart

        
        