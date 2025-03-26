import unittest
import encryptme


class Tests(unittest.TestCase):
    def test_1(self):
        expected = 'Why do elephants have big ears?'
        with open('intercepted_message.txt', 'r') as f:
            message = f.read()
            plain_text = encryptme.decrypt(message)
            self.assertEqual(plain_text, expected)
