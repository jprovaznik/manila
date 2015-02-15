# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Fakes For Scheduler tests.
"""

from oslo_utils import timeutils
import six

from manila.scheduler import filter_scheduler
from manila.scheduler import host_manager

SHARE_SERVICES_NO_POOLS = [
    dict(id=1, host='host1', topic='share', disabled=False,
         availability_zone='zone1', updated_at=timeutils.utcnow()),
    dict(id=2, host='host2@back1', topic='share', disabled=False,
         availability_zone='zone1', updated_at=timeutils.utcnow()),
    dict(id=3, host='host2@back2', topic='share', disabled=False,
         availability_zone='zone2', updated_at=timeutils.utcnow()),
]

SERVICE_STATES_NO_POOLS = {
    'host1': dict(share_backend_name='AAA',
                  total_capacity_gb=512, free_capacity_gb=200,
                  timestamp=None, reserved_percentage=0,
                  driver_handles_share_servers=False),
    'host2@back1': dict(share_backend_name='BBB',
                        total_capacity_gb=256, free_capacity_gb=100,
                        timestamp=None, reserved_percentage=0,
                        driver_handles_share_servers=False),
    'host2@back2': dict(share_backend_name='CCC',
                        total_capacity_gb=10000, free_capacity_gb=700,
                        timestamp=None, reserved_percentage=0,
                        driver_handles_share_servers=False),
}

SHARE_SERVICES_WITH_POOLS = [
    dict(id=1, host='host1@AAA', topic='share', disabled=False,
         availability_zone='zone1', updated_at=timeutils.utcnow()),
    dict(id=2, host='host2@BBB', topic='share', disabled=False,
         availability_zone='zone1', updated_at=timeutils.utcnow()),
    dict(id=3, host='host3@CCC', topic='share', disabled=False,
         availability_zone='zone2', updated_at=timeutils.utcnow()),
    dict(id=4, host='host4@DDD', topic='share', disabled=False,
         availability_zone='zone3', updated_at=timeutils.utcnow()),
    # service on host5 is disabled
    dict(id=5, host='host5@EEE', topic='share', disabled=True,
         availability_zone='zone4', updated_at=timeutils.utcnow()),
]

SHARE_SERVICE_STATES_WITH_POOLS = {
    'host1@AAA': dict(share_backend_name='AAA',
                      timestamp=None, reserved_percentage=0,
                      driver_handles_share_servers=False,
                      pools=[dict(pool_name='pool1',
                                  total_capacity_gb=51,
                                  free_capacity_gb=41,
                                  reserved_percentage=0)]),
    'host2@BBB': dict(share_backend_name='BBB',
                      timestamp=None, reserved_percentage=0,
                      driver_handles_share_servers=False,
                      pools=[dict(pool_name='pool2',
                                  total_capacity_gb=52,
                                  free_capacity_gb=42,
                                  reserved_percentage=0)]),
    'host3@CCC': dict(share_backend_name='CCC',
                      timestamp=None, reserved_percentage=0,
                      driver_handles_share_servers=False,
                      pools=[dict(pool_name='pool3',
                                  total_capacity_gb=53,
                                  free_capacity_gb=43,
                                  reserved_percentage=0)]),
    'host4@DDD': dict(share_backend_name='DDD',
                      timestamp=None, reserved_percentage=0,
                      driver_handles_share_servers=False,
                      pools=[dict(pool_name='pool4a',
                                  total_capacity_gb=541,
                                  free_capacity_gb=441,
                                  reserved_percentage=0),
                             dict(pool_name='pool4b',
                                  total_capacity_gb=542,
                                  free_capacity_gb=442,
                                  reserved_percentage=0)]),
    'host5@EEE': dict(share_backend_name='EEE',
                      timestamp=None, reserved_percentage=0,
                      driver_handles_share_servers=False,
                      pools=[dict(pool_name='pool5a',
                                  total_capacity_gb=551,
                                  free_capacity_gb=451,
                                  reserved_percentage=0),
                             dict(pool_name='pool5b',
                                  total_capacity_gb=552,
                                  free_capacity_gb=452,
                                  reserved_percentage=0)]),
}


class FakeFilterScheduler(filter_scheduler.FilterScheduler):
    def __init__(self, *args, **kwargs):
        super(FakeFilterScheduler, self).__init__(*args, **kwargs)
        self.host_manager = host_manager.HostManager()


class FakeHostManager(host_manager.HostManager):
    def __init__(self):
        super(FakeHostManager, self).__init__()

        self.service_states = {
            'host1': {'total_capacity_gb': 1024,
                      'free_capacity_gb': 1024,
                      'reserved_percentage': 10,
                      'timestamp': None},
            'host2': {'total_capacity_gb': 2048,
                      'free_capacity_gb': 300,
                      'reserved_percentage': 10,
                      'timestamp': None},
            'host3': {'total_capacity_gb': 512,
                      'free_capacity_gb': 512,
                      'reserved_percentage': 0,
                      'timestamp': None},
            'host4': {'total_capacity_gb': 2048,
                      'free_capacity_gb': 200,
                      'reserved_percentage': 5,
                      'timestamp': None},
            'host5': {'total_capacity_gb': 2048,
                      'free_capacity_gb': 500,
                      'reserved_percentage': 5,
                      'timestamp': None},
        }


class FakeHostState(host_manager.HostState):
    def __init__(self, host, attribute_dict):
        super(FakeHostState, self).__init__(host)
        for (key, val) in six.iteritems(attribute_dict):
            setattr(self, key, val)


def mock_host_manager_db_calls(mock_obj, disabled=None):
    services = [
        dict(id=1, host='host1', topic='share', disabled=False,
             availability_zone='zone1', updated_at=timeutils.utcnow()),
        dict(id=2, host='host2', topic='share', disabled=False,
             availability_zone='zone1', updated_at=timeutils.utcnow()),
        dict(id=3, host='host3', topic='share', disabled=False,
             availability_zone='zone2', updated_at=timeutils.utcnow()),
        dict(id=4, host='host4', topic='share', disabled=False,
             availability_zone='zone3', updated_at=timeutils.utcnow()),
        dict(id=5, host='host5', topic='share', disabled=False,
             availability_zone='zone3', updated_at=timeutils.utcnow()),
    ]
    if disabled is None:
        mock_obj.return_value = services
    else:
        mock_obj.return_value = [service for service in services
                                 if service['disabled'] == disabled]
