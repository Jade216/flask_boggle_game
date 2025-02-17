from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn('Score:', res.data)

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"], 
                                    ["C", "A", "T", "T", "T"]]
                
        res = self.client.get('/check-word?word=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsfssffw')
        self.assertEqual(response.json['result'], 'not-word')
    