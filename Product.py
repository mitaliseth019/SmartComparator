class Product:
    def __init__(self,id,name,features,price):
        self.id=id
        self.name=name
        self.features=features
        self.price=price
    def __setattr__(self, __name: str, __value) -> None:
        if __name=="features":
            if len(__value)==0:
                raise AttributeError("Features can not be empty.")
        object.__setattr__(self, __name, __value)