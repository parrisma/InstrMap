import uuid


class GUID:
    def __init__(self):
        self.value = uuid.uuid4()

    def __str__(self): return str(self.value)

    def __eq__(self, other):
        if isinstance(other, GUID):
            return self.value == other.value
        return False

    def __hash__(self): return hash(self.value)
