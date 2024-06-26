from flask import Blueprint


class V1App(Blueprint):
    def __init__(self):
        super().__init__("V1App", __name__)
