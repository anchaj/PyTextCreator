# -*- coding: utf-8 -*-

import abc
from UserString import MutableString

from ServerHTTP import ServerHTTP

result = MutableString()


class Address:
    def __init__(self, street, number, postcode, place):
        self.street = street
        self.number = number
        self.postcode = postcode
        self.place = place


class Element:
    def __init__(self, etype="def"):
        self.etype = etype


class DocumentHeader(Element):
    def __init__(self, atitle, asubtitle, etype="DocumentHeader"):
        Element.__init__(self, etype)
        self.title = atitle
        self.subtitle = asubtitle


class Person(Element):
    def __init__(self, name, surname, address, etype="Person"):
        Element.__init__(self, etype)
        self.name = name
        self.surname = surname
        self.address = address


class Surveyor(Person):
    def __init__(self, name, surname, address, nip, regon, etype="Surveyor"):
        Person.__init__(self, name, surname, address, etype)
        self.nip = nip
        self.regon = regon


class PlainText(Element):
    def __init__(self, text, etype="PlainText"):
        Element.__init__(self, etype)
        self.text = text


class ProtocolStamp(Element):
    def __init__(self, voivodeship, powiat, registry_unit, precinct_name, precinct_number, etype="ProtocolStamp"):
        Element.__init__(self, etype)
        self.voivodeship = voivodeship
        self.powiat = powiat
        self.registry_unit = registry_unit
        self.precinct_name = precinct_name
        self.precinct_number = precinct_number


class TableTags:
    def __init__(self, start_array, end_array, start_row, end_row, start_cell, end_cell):
        self.start_array = start_array
        self.end_array = end_array
        self.start_row = start_row
        self.end_row = end_row
        self.start_cell = start_cell
        self.end_cell = end_cell


class Table(Element):
    def __init__(self, rows, columns=2, etype="Table"):
        Element.__init__(self, etype)
        self.rows = rows
        self.columns = columns


class Printer:
    __metaclass__ = abc.ABCMeta

    def __init__(self, table_tags):
        self.table_tags = table_tags

    @abc.abstractmethod
    def start_center(self):
        """Abstrakcyjna metoda fabryczna, mająca zwrócić
        tag rozpoczęcia wyśrodkowania z podklasy."""
        return

    @abc.abstractmethod
    def end_center(self):
        """Abstrakcyjna metoda fabryczna, mająca zwrócić
        tag zakończenia wyśrodkowania z podklasy."""
        return

    @abc.abstractmethod
    def get_newline(self):
        """Abstrakcyjna metoda fabryczna, mająca zwrócić
        polecenie wydrukowania nowej linii z podklasy."""
        return

    @abc.abstractmethod
    def print_bold(self, text):
        """Abstrakcyjna metoda fabryczna, mająca zwrócić
        pogrubiony tekst z podklasy"""
        return

    def print_element(self, element):

        """

        """

        if isinstance(element, PlainText):
            self.print_plaintext(element)

        if isinstance(element, Surveyor):
            self.print_surveyor(element)

        if isinstance(element, ProtocolStamp):
            self.print_protocol_stamp(element)

        if isinstance(element, DocumentHeader):
            self.print_document_header(element)

        if isinstance(element, Table):
            self.print_table(element)

    def print_plaintext(self, plaintext):
        global result
        result.append(plaintext.text)
        result.append(self.get_newline())

    def print_surveyor(self, surveyor):
        global result
        newline = self.get_newline()
        result.append(self.print_bold("GEODETA UPRAWNIONY"))
        result.append(newline)
        result.append(surveyor.name)
        result.append(" ")
        result.append(surveyor.surname)
        result.append(newline)
        result.append(newline)
        result.append(surveyor.address.postcode)
        result.append(" ")
        result.append(surveyor.address.place)
        result.append(newline)
        result.append("ul. ")
        result.append(surveyor.address.street)
        result.append(" ")
        result.append(surveyor.address.number)
        result.append(newline)
        result.append(newline)
        result.append(self.print_bold("REGON: "))
        result.append(surveyor.regon)
        result.append(newline)
        result.append(self.print_bold("NIP: "))
        result.append(surveyor.nip)
        result.append(newline)

    def print_protocol_stamp(self, protocol_stamp):
        global result
        newline = self.get_newline()
        result.append(self.print_bold("Województwo: "))
        result.append(protocol_stamp.voivodeship)
        result.append(newline)
        result.append(self.print_bold("Powiat: "))
        result.append(protocol_stamp.powiat)
        result.append(newline)
        result.append(self.print_bold("Jednostka ewidencyjna: "))
        result.append(protocol_stamp.registry_unit)
        result.append(newline)
        result.append(self.print_bold("Nazwa obrębu: "))
        result.append(protocol_stamp.precinct_name)
        result.append(newline)
        result.append(self.print_bold("Numer obrębu: "))
        result.append(protocol_stamp.precinct_number)
        result.append(newline)

    def print_document_header(self, document_header):
        global result
        newline = self.get_newline()
        result.append(self.start_center())
        result.append(newline)
        result.append(self.print_bold(document_header.title))
        result.append(newline)
        result.append(document_header.subtitle)
        result.append(newline)
        result.append(self.end_center())
        result.append(newline)

    def print_table(self, table):
        global result
        result.append(self.table_tags.start_array)

        rows = table.rows.split("|")
        for row in rows:
            splitted = row.split(";")

            result.append(self.table_tags.start_row)

            for cell in splitted:
                result.append(self.table_tags.start_cell)
                result.append(cell)
                result.append(self.table_tags.end_cell)

            result.append(self.table_tags.end_row)

        result.append(self.table_tags.end_array)


class HTMLPrinter(Printer):
    html_table_tags = TableTags("<table>\n", "</table>\n", "\t<tr>\n\t\t", "\n\t</tr>\n", "<td>", "</td>")

    instance = None

    def __init__(self):
        Printer.__init__(self, HTMLPrinter.html_table_tags)

    @staticmethod
    def get_instance():
        if HTMLPrinter.instance is None:
            HTMLPrinter.instance = HTMLPrinter()

        return HTMLPrinter.instance

    def start_center(self):
        return "<center>\n"

    def end_center(self):
        return "</center>\n"

    def get_newline(self):
        return "<br>\n"

    def print_bold(self, text):
        res = "<b>" + text + "</b>"
        return res


class TeXPrinter(Printer):
    tex_table_tags = TableTags("\\begin{array}\n", "\n\\end{array}\n", "", "\\\\", "", " & ")

    instance = None

    def __init__(self):
        Printer.__init__(self, TeXPrinter.tex_table_tags)

    @staticmethod
    def get_instance():
        if TeXPrinter.instance is None:
            TeXPrinter.instance = TeXPrinter()

        return TeXPrinter.instance

    def start_center(self):
        return "\\begin{center}"

    def end_center(self):
        return "\\end{center}"

    def get_newline(self):
        return '\\\\\n'

    def print_bold(self, text):
        return "\\textbf{" + text + "}"


class Document:
    def __init__(self):
        self.printer = None
        self.elements = []

    def set_printer(self, printer):
        self.printer = printer

    def append(self, element):
        self.elements.append(element)

    def print_document(self):
        global result

        for el in self.elements:
            self.printer.print_element(el)


class Protocol(Document):
    def __init__(self, protocol_stamp):
        Document.__init__(self)
        self.protocol_stamp = protocol_stamp


class Notification(Document):
    def __init__(self, surveyor):
        Document.__init__(self)
        self.surveyor = surveyor


def print_notification(data):
    global result
    result = MutableString()

    s_address = Address(data["street"][0], data["number"][0], data["place"][0], data["postcode"][0])
    surveyor = Surveyor(data["name"][0], data["surname"][0], s_address, data["nip"][0], data["regon"][0])
    d_header = DocumentHeader("ZAWIADOMIENIE", data["subtitle"][0])
    notification = Notification(surveyor)

    notification.append(surveyor)
    notification.append(d_header)

    result.append('<form method="POST">')
    data['doc_type'][0] = 'notification'
    result.append('<input type="hidden" name="doc_type" value="notification">')
    result.append('<input type="submit" value="Powrót do formularza"/>')
    result.append("</form>")

    result.append("<div id=\"document_result\">")
    notification.set_printer(HTMLPrinter.get_instance())
    notification.print_document()
    result.append("</div><br>")

    result.append("<textarea rows=\"20\" cols=\"85\">")
    notification.set_printer(TeXPrinter.get_instance())
    notification.print_document()
    result.append("</textarea>")

    return result


def print_protocol(data):
    global result
    result = MutableString()
    p_stamp = ProtocolStamp(data["voivodeship"][0],
                            data["powiat"][0],
                            data["registry_unit"][0],
                            data["precinct_name"][0],
                            data["precinct_number"][0])
    d_header = DocumentHeader("PROTOKÓŁ", data["subtitle"][0])

    p_table = Table(data["table"][0])

    protocol = Protocol(p_stamp)

    protocol.append(p_stamp)
    protocol.append(d_header)
    protocol.append(p_table)

    result.append('<form method="POST">')
    data['doc_type'][0] = 'protocol'
    result.append('<input type="hidden" name="doc_type" value="protocol">')
    result.append('<input type="submit" value="Powrót do formularza"/>')
    result.append("</form>")

    result.append("<div id=\"document_result\">")
    protocol.set_printer(HTMLPrinter.get_instance())
    protocol.print_document()
    result.append("</div><br>")

    result.append("<textarea rows=\"20\" cols=\"85\">")
    protocol.set_printer(TeXPrinter.get_instance())
    protocol.print_document()
    result.append("</textarea>")

    return result


def get_html(path):
    with open(path, "r") as myfile:
        data = myfile.read().replace('\n', '')
    return data


def changer(data):
    result_html = get_html("result.html")

    if data["doc_type"][0] == "notification":
        return get_html("notification.html")

    if data["doc_type"][0] == "notification_submit":
        return result_html + print_notification(data)

    if data["doc_type"][0] == "protocol":
        return get_html("protocol.html")

    if data["doc_type"][0] == "protocol_submit":
        return result_html + print_protocol(data)

    return "unexpected"


def main():
    server = ServerHTTP(handler_on_post_callable=changer)
    server.start()


if __name__ == "__main__":
    main()
