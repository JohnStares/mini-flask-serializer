
class Database1:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    

class Database2:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }



class Database3:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self._is_active = True


