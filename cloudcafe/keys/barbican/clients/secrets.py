"""
Copyright 2013-2014 Rackspace

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
from cloudcafe.keys.barbican.clients.base import BarbicanBaseClient
from cloudcafe.keys.barbican.models.secrets import Secret
from cloudcafe.keys.barbican.models.secrets import SecretRef
from cloudcafe.keys.barbican.models.secrets import SecretMetadata
from cloudcafe.keys.barbican.models.secrets import SecretGroup


class SecretsClient(BarbicanBaseClient):
    def __init__(self, url, api_version, tenant_id, token=None,
                 serialize_format=None, deserialize_format=None):
        super(SecretsClient, self).__init__(
            token=token,
            serialize_format=serialize_format,
            deserialize_format=deserialize_format)

        self.url = url
        self.api_version = api_version
        self.tenant_id = tenant_id

    @property
    def base_url(self):
        return '{base}/{api_version}/{tenant_id}/secrets'.format(
            base=self.url,
            api_version=self.api_version,
            tenant_id=self.tenant_id)

    def create_secret(self, name=None, expiration=None, algorithm=None,
                      bit_length=None, mode=None, payload=None,
                      payload_content_type=None,
                      payload_content_encoding=None):
        """
        POST http://.../v1/{tenant_id}/secrets
        Allows a user to create a new secret
        """
        req_obj = Secret(name=name, payload_content_type=payload_content_type,
                         payload_content_encoding=payload_content_encoding,
                         expiration=expiration, algorithm=algorithm,
                         bit_length=bit_length, mode=mode,
                         payload=payload)

        resp = self.request('POST', self.base_url, request_entity=req_obj,
                            response_entity_type=SecretRef)

        return resp

    def create_secret_with_no_json(self):
        """ Create secret but do not pass any JSON."""
        return self.request('POST', self.base_url,
                            response_entity_type=SecretRef)

    def add_secret_payload(self, secret_ref, payload_content_type, payload,
                           payload_content_encoding=None):
        """ PUT http://.../v1/{tenant_id}/secrets/{secret_uuid}
        Allows the user to upload secret data for a specified secret if
        the secret doesn't already exist

        :param secret_ref: HATEOAS ref of the target secret.
        """
        headers = {
            'Content-Type': payload_content_type,
            'Content-Encoding': payload_content_encoding
        }

        return self.request('PUT', secret_ref, headers=headers, data=payload)

    def get_secret(self, secret_ref, payload_content_type=None,
                   payload_content_encoding=None):
        """
        GET http://.../v1/{tenant_id}/secrets/{secret_uuid}

        :param secret_ref: HATEOAS ref of the target secret.
        :param payload_content_type: if not set, it'll only retrieve
        the metadata for the secret.
        """
        resp_type = None
        if payload_content_type is None:
            resp_type = SecretMetadata
            payload_content_type = 'application/json'

        headers = {
            'Accept': payload_content_type,
            'Accept-Encoding': payload_content_encoding
        }

        return self.request('GET', secret_ref, headers=headers,
                            response_entity_type=resp_type)

    def get_secrets(self, limit=None, offset=None):
        """ GET http://.../v1/secrets?limit={limit}&offset={offset} or {ref}
        Gets a list of secrets
        """
        params = {
            'limit': limit,
            'offset': offset
        }

        return self.request('GET', self.base_url, params=params,
                            response_entity_type=SecretGroup)

    def delete_secret(self, secret_ref):
        """ Makes a DELETE call to the passed in secret_ref

        :param secret_ref: HATEOAS ref of the target secret.
        """
        return self.request('DELETE', secret_ref)
