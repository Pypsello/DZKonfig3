import argparse
import xml.etree.ElementTree as ET
import sys
import re


class ConfigLanguageConverter:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.output = []

    def parse_xml(self):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            self.process_element(root)
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
            sys.exit(1)

    def process_element(self, element):
        # Обработка многострочных комментариев
        if element.tag == "comment":
            self.output.append(f"|# {element.text.strip()} #|")
            return

        # Обработка словарей
        if element.tag == "dict":
            dict_name = element.attrib.get('name')
            dict_values = []
            for child in element:
                if child.tag == "item":
                    name = child.attrib.get('name')
                    value = child.text.strip()
                    dict_values.append(f"{name} = {value}")
                else:
                    self.report_error(f"Неизвестный элемент в словаре: {child.tag}")
            dict_content = ', '.join(dict_values)
            self.output.append(f"dict({dict_content})")

        # Обработка констант
        elif element.tag == "const":
            const_name = element.attrib.get('name')
            const_value = element.text.strip()
            self.output.append(f"def {const_name} = {const_value};")

        # Обработка вычислений
        elif element.tag == "compute":
            const_name = element.attrib.get('name')
            self.output.append(f"?{{{const_name}}}")

        # Рекурсивная обработка дочерних элементов
        for child in element:
            self.process_element(child)

    def report_error(self, message):
        print(f"Ошибка: {message}")
        sys.exit(1)

    def get_output(self):
        return "\n".join(self.output)

def main():
    parser = argparse.ArgumentParser(description="Конвертер XML в учебный конфигурационный язык.")
    parser.add_argument("xml_file", help="Путь к файлу XML для обработки.")
    args = parser.parse_args()

    converter = ConfigLanguageConverter(args.xml_file)
    converter.parse_xml()
    output = converter.get_output()
    print(output)


if __name__ == "__main__":
    main()

