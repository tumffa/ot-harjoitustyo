import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_lataaminen_kasvattaa_oikein(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 11)

    def test_rahan_ottaminen_toimii_kun_tarpeeksi_saldoa(self):
        self.maksukortti.ota_rahaa(900)
        self.assertEqual(self.maksukortti.saldo_euroina(), 1)

    def test_rahan_ottaminen_ei_toimi_kun_ei_tarpeeksi_saldoa(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_rahan_ottaminen_palauttaa_true(self):
        vastaus = self.maksukortti.ota_rahaa(900)
        self.assertEqual(vastaus, True)
    
    def test_rahan_ottaminen_palauttaa_true(self):
        vastaus = self.maksukortti.ota_rahaa(1500)
        self.assertEqual(vastaus, False)

    def test_maksukortin_tulostus_toimii(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")