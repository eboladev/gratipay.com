from __future__ import print_function, unicode_literals

from aspen import json
from gratipay.testing import Harness


class Tests(Harness):

    def setUp(self):
        Harness.setUp(self)
        self.make_participant('alice')

    def hit_anonymous(self, method='GET', expected_code=200, **kw):
        response = self.client.hit(method, "/alice/anonymous.json", auth_as='alice', **kw)
        if response.code != expected_code:
            print(response.body)
        return response


    def test_participant_can_get_their_anonymity_settings(self):
        response = self.hit_anonymous('GET')
        actual = json.loads(response.body)
        assert actual == {'giving': False, 'receiving': False, 'supporters': True}

    def test_participant_can_toggle_anonymous_giving(self):
        response = self.hit_anonymous('POST', data={'toggle': 'giving'})
        actual = json.loads(response.body)
        assert actual['giving'] is True

    def test_participant_can_toggle_anonymous_receiving(self):
        response = self.hit_anonymous('POST', data={'toggle': 'receiving'})
        actual = json.loads(response.body)
        assert actual['receiving'] is True

    def test_participant_can_toggle_anonymous_supporters(self):
        response = self.hit_anonymous('POST', data={'toggle': 'supporters'})
        actual = json.loads(response.body)
        assert actual['supporters'] is False

    def test_team_cannot_toggle_anonymous_receiving(self):
        self.make_participant('team', number='plural')
        response = self.client.PxST(
            '/team/anonymous.json',
            auth_as='team',
            data={'toggle': 'receiving'}
        )
        actual = response.code
        expected = 400
        assert actual == expected

    def test_team_can_toggle_anonymous_supporters(self):
        self.make_participant('team', number='plural')
        response = self.client.POST(
            '/team/anonymous.json',
            auth_as='team',
            data={'toggle': 'supporters'}
        )
        assert json.loads(response.body)['supporters'] == False

    def test_participant_can_toggle_anonymous_giving_back(self):
        response = self.hit_anonymous('POST', data={'toggle': 'giving'})
        response = self.hit_anonymous('POST', data={'toggle': 'giving'})
        actual = json.loads(response.body)['giving']
        assert actual is False

    def test_participant_can_toggle_anonymous_receiving_back(self):
        response = self.hit_anonymous('POST', data={'toggle': 'receiving'})
        response = self.hit_anonymous('POST', data={'toggle': 'receiving'})
        actual = json.loads(response.body)['receiving']
        assert actual is False

    def test_participant_can_toggle_anonymous_supporters_back(self):
        response = self.hit_anonymous('POST', data={'toggle': 'supporters'})
        response = self.hit_anonymous('POST', data={'toggle': 'supporters'})
        actual = json.loads(response.body)['supporters']
        assert actual is True
