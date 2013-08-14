"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from cafe.engine.clients.rest import AutoMarshallingRestClient
from cloudcafe.meniscus.status_api.models.status \
    import WorkerLoadAverage, WorkerDiskUsage, AllWorkersStatus, WorkerStatus


class WorkerStatusClient(AutoMarshallingRestClient):

    def __init__(self, url, api_version, serialize_format,
                 deserialize_format):
        super(WorkerStatusClient, self).__init__(serialize_format,
                                                 deserialize_format)
        self.url = url
        self.api_version = api_version

    def _get_remote_url(self, worker_id):
        url = '{base}/{version}/worker/{worker_id}/status'.format(
            base=self.url, version=self.api_version, worker_id=worker_id)
        return url

    def update_load(self, worker_id, worker_token, one, five, fifteen):
        url = self._get_remote_url(worker_id)
        req_obj = WorkerLoadAverage(one, five, fifteen)
        headers = {'WORKER-TOKEN': worker_token}
        resp = self.request('PUT', url, headers=headers,
                            request_entity=req_obj)
        return resp

    def update_usage(self, worker_id, worker_token, disks):
        url = self._get_remote_url(worker_id)
        req_obj = WorkerDiskUsage._dict_to_obj(disks)
        headers = {'WORKER-TOKEN': worker_token}
        resp = self.request('PUT', url, headers=headers,
                            request_entity=req_obj)
        return resp

    def direct_update(self, worker_id, worker_token, body):
        """Allows direct access for negative testing ONLY!"""
        url = self._get_remote_url(worker_id)
        headers = {'WORKER-TOKEN': worker_token}
        return self.request('PUT', url, headers=headers)

    def get_worker_status(self, worker_id):
        url = '{base}/{version}/worker/{worker_id}/status'.format(
            base=self.url, version=self.api_version, worker_id=worker_id)
        resp = self.request('GET', url, response_entity_type=WorkerStatus)
        return resp

    def get_all_worker_statuses(self):
        url = '{base}/{version}/status'.format(base=self.url,
                                               version=self.api_version)
        resp = self.request('GET', url, response_entity_type=AllWorkersStatus)
        return resp
