class InvalidId(Exception):
    def get_json_repr(self):
        return str(self)