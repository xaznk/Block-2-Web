import json
import pickle as pkl
from abc import abstractmethod, ABC


class SerializationBaseClass(ABC):
    @abstractmethod
    def serialize(self, data):
        self.data = data


class JSONSerialization(SerializationBaseClass):
    def serialize(data):
        with open('json.json', 'w') as f:
            json.dump(data, f)

        with open('json.json', 'r') as f:
            data = json.load(f)
            return data


class BinSerialization(SerializationBaseClass):
    def serialize(data):
        with open('bin.bin', 'wb') as f:
            pkl.dump(data, f)

        with open('bin.bin', 'rb') as f:
            data = pkl.load(f)
            return data

        
a = JSONSerialization.serialize(['12345678', 12312, '12412573'])
print(a)
b = BinSerialization.serialize('1421')
print(b)
