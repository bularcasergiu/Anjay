# -*- coding: utf-8 -*-
#
# Copyright 2017 AVSystem <avsystem@avsystem.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from framework.lwm2m_test import *


class UriChangeUpdateTest(test_suite.Lwm2mTest):
    def setUp(self):
        self.setup_demo_with_servers(servers=2,
                                     num_servers_passed=1,
                                     bootstrap_server=True,
                                     auto_register=False)

    def tearDown(self):
        self.teardown_demo_with_servers(deregister_servers=[self.servers[1]])

    def runTest(self):
        regular_serv1_uri = 'coap://127.0.0.1:%d' % self.servers[0].get_listen_port()
        regular_serv2_uri = 'coap://127.0.0.1:%d' % self.servers[1].get_listen_port()

        # Register to regular_serv1
        pkt = self.servers[0].recv(timeout_s=1)
        self.assertMsgEqual(
            Lwm2mRegister('/rd?lwm2m=%s&ep=%s&lt=86400' % (DEMO_LWM2M_VERSION, DEMO_ENDPOINT_NAME)),
            pkt)
        self.servers[0].send(Lwm2mCreated.matching(pkt)(location='/rd/demo'))

        req = Lwm2mDiscover('/0')
        self.servers[0].send(req)
        res = self.servers[0].recv()
        self.assertMsgEqual(Lwm2mContent.matching(req)(), res)

        self.assertIn(b'</0/1/', res.content)
        self.assertIn(b'</0/2/', res.content)

        # modify the server URI
        demo_port = int(self.communicate('get-port -1', match_regex='PORT==([0-9]+)\n').group(1))
        self.bootstrap_server.connect(('127.0.0.1', demo_port))

        req = Lwm2mWrite('/0/2/%d' % RID.Security.ServerURI,
                         regular_serv2_uri)
        self.bootstrap_server.send(req)

        self.assertMsgEqual(Lwm2mChanged.matching(req)(),
                            self.bootstrap_server.recv())

        # send Bootstrap Finish - trigger notifications
        req = Lwm2mBootstrapFinish()
        self.bootstrap_server.send(req)

        self.assertMsgEqual(Lwm2mChanged.matching(req)(),
                            self.bootstrap_server.recv())

        # we should now get a Registration Update on the new URL
        self.assertDemoUpdatesRegistration(self.servers[1])
