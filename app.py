"""Simple app to monitor Roudor stock
Add box of roudor Because we by it by box
Delete box X persone take one packet so delete the box
Delete Packet we can eat a whole packet
Delete Roudor Because we can eat one roudor
"""
import datetime
from flask import request
from flask_api import FlaskAPI

class FileLogger:
    def __init__(self, file_path):
        self.log_full_path = file_path
    def log(self, message):
        with open(self.log_full_path, 'a') as log_file:
            log_file.write(message)

class Stock(FileLogger):
    def __init__(self):
        self.roudors = 0
        self.roudor_per_packet = 3
        self.packet_per_box = 4
        self.logger = FileLogger('/tmp/roudor.log')

    def __add_roudors(self, nb_roudors):
        self.roudors += nb_roudors

    def __delete_roudors(self, nb_roudors):
        self.roudors -= nb_roudors

    def get_roudors_from_packets(self, nb_packets):
        return nb_packets * self.roudor_per_packet

    def get_roudors_from_box(self, nb_box):
        return nb_box * self.packet_per_box * self.roudor_per_packet

    def add_box(self, nb_box):
        roudors_to_add = self.get_roudors_from_box(nb_box)
        self.__add_roudors(roudors_to_add)
        self.log_add_box(nb_box)

    def delete_box(self, nb_box):
        roudors_to_delete = self.get_roudors_from_box(nb_box)
        self.log_delete_box(nb_box)
        self.__delete_roudors(roudors_to_delete)
        self.log_delete_box(nb_box)

    def delete_packets(self, nb_packet):
        roudors_to_delete = self.get_roudors_from_packets(nb_packet)
        self.__delete_roudors(roudors_to_delete)
        self.log_delete_packets(nb_packet)

    def delete_roudors(self, nb_roudors):
        roudors_to_delete = nb_roudors
        self.__delete_roudors(roudors_to_delete)
        self.log_delete_roudors(nb_roudors)

    def get_roudors(self):
        return self.roudors

    def get_current_date(self):
        return datetime.datetime.now().isoformat()

    def log_delete_roudors(self, nb_roudors):
        current_date = self.get_current_date()
        message = "%s %d has been eaten %d roudors left\n" % (current_date, nb_roudors, self.roudors)
        self.logger.log(message)

    def log_delete_packets(self, nb_packets):
        current_date = self.get_current_date()
        message = "%s %d packets has been eaten %d roudors left\n" % (current_date, nb_packets, self.roudors)
        self.logger.log(message)

    def log_delete_box(self, nb_box):
        current_date = self.get_current_date()
        message = "%s %d box has been eaten %d roudors left\n" % (current_date, nb_box, self.roudors)
        self.logger.log(message)

    def log_add_box(self, nb_box):
        current_date = self.get_current_date()
        message = "%s %d box has been added %d roudors left\n" % (current_date, nb_box, self.roudors)
        self.logger.log(message)


app = FlaskAPI(__name__)

STOCK = Stock()


@app.route('/roudors', methods=['DELETE'])
def delete_roudors():
    number_of_roudors = request.json['quantity']
    STOCK.delete_roudors(number_of_roudors)
    return {"roudors": STOCK.get_roudors()}


@app.route('/packet', methods=['DELETE'])
def delete_packets():
    number_of_packets = request.json['quantity']
    STOCK.delete_packets(number_of_packets)
    return {"roudors": STOCK.get_roudors()}


@app.route('/box', methods=['DELETE'])
def delete_box():
    number_of_box = request.json['quantity']
    STOCK.delete_box(number_of_box)
    return {"roudors": STOCK.get_roudors()}


@app.route('/box', methods=['POST'])
def add_box():
    number_of_box = request.json['quantity']
    STOCK.add_box(number_of_box)
    return {"roudors": STOCK.get_roudors()}


@app.route("/roudors", methods=['GET'])
def roudors():
    return {"roudors": STOCK.get_roudors()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



