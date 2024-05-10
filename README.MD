# Laskinsovellus

Laskinsovellus, jolla pystyy suorittamaan matemaattisia lausekkeita komentoriviltä käsin.

- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Changelog](./dokumentaatio/changelog.md)
- [Tuntikirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)
- [Käyttöohje](./dokumentaatio/kayttoohje.md)

## Releaset
- [Viikko 7](https://github.com/tumffa/ot-harjoitustyo/releases/tag/viikko7)
- [Viikko 6](https://github.com/tumffa/ot-harjoitustyo/releases/tag/viikko6)
- [Viikko 5](https://github.com/tumffa/ot-harjoitustyo/releases/tag/viikko5)

## Asennusohjeet

Sinulla tulee olla asennettuna
>poetry
>
>python "^3.8"

Lataa release ylhäältä ja pura tiedosto

Navigoi projektin juurihakemistoon ja suorita komento
```shell
poetry install
```

## Tasks-komennot

Sovelluksen voi käynnistää komennolla
```shell
poetry run invoke start
```

Yksikkötestit voi suorittaa komennolla
```shell
poetry run invoke pytest
```

Testikattavuusraportin saa komennolla
```shell
poetry run invoke coverage-report
```

Pylint-testit voi suorittaa komennolla
```shell
poetry run invoke lint
```
