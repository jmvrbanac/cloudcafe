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
from json import dumps as json_to_str, loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel


class UpdateProducer(AutoMarshallingModel):

    def __init__(self, producer_name=None, producer_pattern=None,
                 producer_durable=None, producer_encrypted=None):
        super(UpdateProducer, self).__init__()

        self.name = producer_name
        self.pattern = producer_pattern
        self.durable = producer_durable
        self.encrypted = producer_encrypted

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        body = {
            'name': self.name,
            'pattern': self.pattern,
            'durable': self.durable,
            'encrypted': self.encrypted
        }
        return {'event_producer': self._remove_empty_values(body)}


# Create requires all parameters, whereas update they are optional
class CreateProducer(UpdateProducer):
    def __init__(self, producer_name, producer_pattern,
                 producer_durable, producer_encrypted):
        super(CreateProducer, self).__init__(producer_name, producer_pattern,
                                             producer_durable,
                                             producer_encrypted)


class Producer(AutoMarshallingModel):
    ROOT_TAG = 'event_producer'

    def __init__(self, pattern=None, durable=None, encrypted=None, id=None,
                 name=None, sinks=None):
        super(Producer, self).__init__()
        self.pattern = pattern
        self.durable = durable
        self.encrypted = encrypted
        self.id = id
        self.name = name
        self.sinks = sinks

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Producer(**json_dict)


class AllProducers(AutoMarshallingModel):
    ROOT_TAG = 'event_producers'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)

        converted = []
        json_producer_list = json_dict.get(cls.ROOT_TAG)

        for json_producer in json_producer_list:
            producer = Producer._dict_to_obj(json_producer)
            converted.append(producer)

        return converted
