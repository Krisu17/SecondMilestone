import uuid

from fpdf import FPDF


class Waybill:

    def __init__(self, sender, recipient):
        self.__sender = sender
        self.__recipient = recipient

    def generate_and_save(self, path="./"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        filename = self.__generate_filename(path)
        self.__add_table_to_pdf(pdf, filename)

        
        pdf.output(filename)

        return filename

    def __add_table_to_pdf(self, pdf, fn):
        n_cols = 2
        col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / n_cols / 2
        font_size = pdf.font_size
        n_lines = 6

        
        
        pdf.cell(col_width, n_lines * font_size, "Sender", border=1)
        pdf.multi_cell(col_width, font_size, txt=self.__sender.str_full(), border=1)
        pdf.ln(0)
        pdf.cell(col_width, n_lines * font_size, "Recipient", border=1)
        pdf.multi_cell(col_width, font_size, txt=self.__recipient.str_full(), border=1)
        pdf.ln(0)
        pdf.cell(col_width*2, n_lines * font_size, fn, border=1)

    def __generate_filename(self, path):
        unique_filename = uuid.uuid4().hex

        return "{}{}.pdf".format(path, unique_filename)


class Person:

    def __init__(self, name: str, surname: str, address):
        self.__name = name
        self.__surname = surname
        self.__address = address

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_fullname(self):
        return "{} {}".format(self.__name, self.__surname)

    def get_address(self):
        return self.__address

    def str_full(self):
        return "{}\n{}".format(self.get_fullname(), self.__address.str_full())


class Address:

    def __init__(self, street: str, city: str, postal_code: str, country: str):
        self.__street = street
        self.__city = city
        self.__postal_code = postal_code
        self.__country = country

    def get_street(self):
        return self.__street

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code

    def get_country(self):
        return self.__country

    def str_full(self):
        result = ""
        for field_value in self.__dict__.values():
            result += "\n{}".format(field_value)

        return result