import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
  def setUp(self):
      self.kassapaate = Kassapaate()
      self.kortti = Maksukortti(1000)

  def test_alustettu_oikein(self):
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                          self.kassapaate.edulliset+self.kassapaate.maukkaat),
                            (100000, 0))
      
  def test_edullinen_toimii_kun_varaa(self):
      vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(250)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                          self.kassapaate.edulliset,
                          vaihtoraha),
                            (100240, 1, 10))
      
  def test_maukas_toimii_kun_varaa(self):
      vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(410)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                          self.kassapaate.maukkaat,
                          vaihtoraha),
                            (100400, 1, 10))
      
  def test_edullinen_toimii_kun_ei_varaa(self):
      vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(230)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                          self.kassapaate.edulliset,
                          vaihtoraha),
                            (100000, 0, 230))
  
  def test_maukas_toimii_kun_ei_varaa(self):
      vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(390)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                          self.kassapaate.maukkaat,
                          vaihtoraha),
                            (100000, 0, 390))
      
  def test_edullinen_toimii_kortilla_kun_varaa(self):
      vastaus = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                        self.kortti.saldo_euroina(),
                        self.kassapaate.edulliset,
                        vastaus),
                          (100000, 7.6, 1, True))
      
  def test_maukas_toimii_kortilla_kun_varaa(self):
      vastaus = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                        self.kortti.saldo_euroina(),
                        self.kassapaate.maukkaat,
                        vastaus),
                          (100000, 6, 1, True))
      
  def test_edullinen_toimii_kortilla_kun_ei_varaa(self):
      kortti = Maksukortti(100)
      vastaus = self.kassapaate.syo_edullisesti_kortilla(kortti)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                        kortti.saldo_euroina(),
                        self.kassapaate.edulliset,
                        vastaus),
                          (100000, 1, 0, False))
      
  def test_maukas_toimii_kortilla_kun_ei_varaa(self):
      kortti = Maksukortti(100)
      vastaus = self.kassapaate.syo_maukkaasti_kortilla(kortti)
      self.assertEqual((self.kassapaate.kassassa_rahaa,
                        kortti.saldo_euroina(),
                        self.kassapaate.maukkaat,
                        vastaus),
                          (100000, 1, 0, False))
  
  def test_rahan_lataaminen_toimii_kun_positiivinen(self):
      self.kassapaate.lataa_rahaa_kortille(self.kortti, 100)
      self.assertEqual((self.kassapaate.kassassa_rahaa_euroina(),
                        self.kortti.saldo_euroina()),
                          (1001, 11))
  
  def test_rahan_lataaminen_ei_toimi_kun_negatiivinen(self):
      self.kassapaate.lataa_rahaa_kortille(self.kortti, -100)
      self.assertEqual((self.kassapaate.kassassa_rahaa_euroina(),
                        self.kortti.saldo_euroina()),
                          (1000, 10))