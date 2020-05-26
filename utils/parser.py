import zipfile
from lxml import html
from io import StringIO

from utils.common_config import logger


class WiFiMeta(object):
    """
    :param delimieter: 分隔符， 字段之间的分割
    :param linefeed: 行分割
    """

    def __init__(self, source_info=None, fields=None, field_english=None):
        self.source_info = source_info
        self.fields = fields
        self.field_english = field_english

    @classmethod
    def from_xml(cls, xml: StringIO):
        """

        """
        ht = html.etree.parse(xml, html.etree.HTMLParser())
        source_info = ht.xpath(r'//data/dataset[@name="WA_COMMON_010013"]/data/item/@val')
        fields = ht.xpath(r'//data/dataset/data/dataset[@name="WA_COMMON_010015"]/data/item/@key')
        field_english = ht.xpath(r'//data/dataset/data/dataset[@name="WA_COMMON_010015"]/data/item/@eng')
        return WiFiMeta(source_info, fields, field_english)


class CSVParser:
    def __init__(self, data, meta: WiFiMeta):
        self.data = data
        self.meta = meta

    @property
    def reader(self):
        try:
            data_list = []
            for a in self.data:
                b = a.split('\n')
                b.remove('')
                for i in b:
                    data_list.append([j.strip() for j in [i.split('\t')][0]])
            num = len(self.meta.fields)
            fields = self.meta.field_english
            csv_list = []
            for data in data_list:
                i = 0
                csv_dict = {}
                while i < num:
                    csv_dict[fields[i].lower()] = data[i]
                    i += 1
                csv_list.append(csv_dict)
        except Exception as e:
            logger.error(e)
            return
        return csv_list, self.meta

    @classmethod
    def from_zip(cls, zipinfo):
        data_list = []
        if zipfile.is_zipfile(zipinfo):
            with zipfile.ZipFile(zipinfo) as myzip:
                zip_file = myzip.namelist()
                if zip_file:
                    for file in zip_file:
                        if file.endswith(".xml"):
                            if myzip.open(file):
                                print(zipinfo)
                                meta = WiFiMeta.from_xml(myzip.open(file))
                            else:
                                return
                        elif file.endswith(".bcp"):
                            if myzip.open(file):
                                f = StringIO()
                                for row in myzip.open(file):
                                    row = row.decode("utf-8")
                                    f.write(row)
                                a = f.getvalue()
                                data_list.append(a)
                            else:
                                return
                        return CSVParser(data_list, meta)
                return
        return
