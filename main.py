from gui import main_window
import xml_parser

if __name__ == '__main__':
    xp = xml_parser.XmlParser('price_data.xml')
    main_window.MainWindow(xp)

