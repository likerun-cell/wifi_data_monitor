from typing import Dict

from utils.common_config import logger

WIFI_SOURCE_VALIDATION_INFO = {
    "mac": [str, 17, True], "brand": [str, 128, False], "cache_ssid": [str, 64, False], "capture_time": [int, 20, True],
    "terminal_field_strength": [str, 8, True], "identification_type": [int, 1, False],
    "certificate_code": [str, 64, False],
    "ssid_position": [str, 256, False], "access_ap_mac": [str, 17, False], "access_ap_channel": [str, 5, False],
    "access_ap_encryption_type": [str, 5, False], "x_coordinate": [str, 8, False], "y_coordinate": [str, 8, False],
    "netbar_wacode": [str, 14, True], "collection_equipment_id": [str, 21, True],
    "collection_equipment_longitude": [str, 10, True], "collection_equipment_latitude": [str, 10, True]

}
WIFI_BASIC_VALIDATION_INFO = {
    "netbar_wacode": [str, 14, True], "place_name": [str, 256, True], "site_address": [str, 256, True],
    "longitude": [str, 10, False], "latitude": [str, 10, False], "netsite_type": [str, 5, True],
    "business_nature": [str, 5, False], "law_principal_name": [str, 128, False],
    "law_principal_certificate_type": [str, 5, False], "law_principal_certificate_id": [str, 128, False],
    "relationship_account": [str, 128, False], "start_time": [str, 5, False], "end_time": [str, 5, False],
    "security_software_orgcode": [str, 9, True]
}


class ValidationError(Exception):
    """"
    验证不通过
    """
    def __init__(self, error):
        self.error = error

    @property
    def raise_error(self):
        raise Exception(self.error)


class WiFiData:
    def __init__(self, initial: Dict, meta):
        self._initial = initial
        self.meta = meta  #

        self._clean()

    def _clean(self):
        """验证并尝试转化wifi数据

        :raise: ValueError, 数据值没有通过验证
        """

        if "WA_SOURCE_FJ_1001" in self.meta.source_info:
            validate_data_info = WIFI_SOURCE_VALIDATION_INFO
            self.validate_operate(validate_data_info)
        elif "WA_BASIC_FJ_1003" in self.meta.source_info:
            validate_data_info = WIFI_BASIC_VALIDATION_INFO
            self.validate_operate(validate_data_info)

    def validate_operate(self, validate_data_info):
        errors = []
        for attr in validate_data_info.keys():
            try:
                getattr(self, 'validate_source')(validate_data_info, attr, self._initial[attr])
            except ValidationError as e:
                errors.append(e.args)
                logger.info(e)
        if errors:
            return

    def validate_source(self, validate_data_info, attr, value):
        result = validate_data_info.get(attr)
        if not value:
            if not result[2]:
                self._initial[attr] = None
                return
            else:
                raise ValidationError("此字段属于必填")
        if not isinstance(value, result[0]):
            if result[0] == int:
                self._initial[attr] = int(value)
            else:
                raise ValidationError("数值类型错误")
        if len(value) > result[1]:
            if result[2]:
                raise ValidationError("超过最大长度限制")
            else:
                self._initial[attr] = None

    def to_tuple(self):
        return self._initial

    # @staticmethod
    # def to_pg_many_tuple(wifis):
    #     data_list = []
    #     for wifi in wifis:
    #         result = []
    #         for value in wifi.values():
    #             result.append(value)
    #         data_list.append(tuple(result))
    #     return data_list
