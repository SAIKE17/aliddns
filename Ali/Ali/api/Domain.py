# 调用示例
# from api.Domain import Domain
#
# dolmen = Domain()
# res = dolmen.getDescribeDomainRecordsRequest(params)
# res = dolmen.updateDomainRecordRequest(params)

from . import Sdk
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest


class Domain(Sdk.Sdk):
    def __init__(self):
        super(Domain, self).__init__()
        self.client = AcsClient(self.key_id, self.secret, 'cn-shenzhen')

    def get_describe_domain_records_request(self, params):
        request = DescribeDomainRecordsRequest()
        request.set_DomainName(params['domain_name'])
        return self._res(request, 'DescribeDomainRecords')

    def update_domain_record_request(self, params):
        request = UpdateDomainRecordRequest()
        request.set_RR(params['rr'])
        request.set_RecordId(params['record_id'])
        request.set_Type(params['type'])
        request.set_Value(params['ip'])
        request.set_accept_format('json')
        return self._res(request, 'UpdateDomainRecordRequest')

    def _res(self, request, mth):
        response = self.client.do_action_with_exception(request)
        self.record(response, mth)
        return response
