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
import re
from json import dumps as dict_to_str, loads as str_to_dict
from cafe.engine.models.base import AutoMarshallingModel


class Secret(AutoMarshallingModel):

    def __init__(self, name, expiration, algorithm, bit_length, mode,
                 payload_content_type=None, payload=None, content_types=None,
                 payload_content_encoding=None):
        super(Secret, self).__init__()

        self.name = name
        self.payload_content_type = payload_content_type
        self.expiration = expiration
        self.algorithm = algorithm
        self.bit_length = bit_length
        self.mode = mode
        self.payload = payload
        self.content_types = content_types
        self.payload_content_encoding = payload_content_encoding

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        converted = {
            'name': self.name,
            'expiration': self.expiration,
            'algorithm': self.algorithm,
            'bit_length': self.bit_length,
            'mode': self.mode,
            'payload': self.payload,
            'payload_content_type': self.payload_content_type,
            'payload_content_encoding': self.payload_content_encoding,
            'content_types': self.content_types
        }
        return self._remove_empty_values(converted)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        """ This overridden by SecretMetadata """
        return Secret(**json_dict)


class SecretMetadata(Secret):

    def __init__(self, name, expiration, algorithm, bit_length, mode,
                 payload_content_type=None, payload=None, status=None,
                 updated=None, created=None, secret_ref=None,
                 content_types=None, content_encodings=None):
        super(SecretMetadata, self).__init__(
            name, expiration, algorithm, bit_length, mode,
            payload_content_type, payload, content_types, content_encodings)
        self.status = status
        self.updated = updated
        self.created = created
        self.secret_ref = secret_ref

    def __eq__(self, other):
        return other.secret_ref == self.secret_ref

    def __ne__(self, other):
        return not self == other

    def _obj_to_dict(self):
        converted = super(SecretMetadata, self)._obj_to_dict()

        metadata = {
            'status': self.status,
            'updated': self.updated,
            'created': self.created,
            'secret_ref': self.secret_ref
        }

        # Clean up the metadata and update converted dict
        metadata = self._remove_empty_values(metadata)
        converted.update(metadata)

        return converted

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return SecretMetadata(**json_dict)


class SecretRef(AutoMarshallingModel):

    def __init__(self, reference):
        super(SecretRef, self).__init__()
        self.reference = reference

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return SecretRef(reference=json_dict.get('secret_ref'))


class UpdateSecret(AutoMarshallingModel):

    def __init__(self, payload):
        super(UpdateSecret, self).__init__()
        self.payload = payload

    def _obj_to_json(self):
        return dict_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {'payload': self.payload}


class SecretGroup(AutoMarshallingModel):

    def __init__(self, secrets, next_list=None, previous_list=None):
        super(SecretGroup, self).__init__()

        self.secrets = secrets
        self.next = next_list
        self.previous = previous_list

    def get_next_query_data(self):
        matches = re.search('.*\?(.*?)\=(\d*)&(.*?)\=(\d*)', self.next)
        return {
            'limit': matches.group(2),
            'offset': matches.group(4)
        }

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_dict(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        secrets, next_list, prev_list = [], None, None

        for secret_dict in json_dict.get('secrets'):
            secrets.append(SecretMetadata._dict_to_obj(secret_dict))

        if 'next' in json_dict:
            next_list = json_dict.get('next')
        if 'previous' in json_dict:
            prev_list = json_dict.get('previous')
        return SecretGroup(secrets, next_list, prev_list)
