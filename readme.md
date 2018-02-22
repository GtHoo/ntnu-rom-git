For å kjøre scriptet:
```bash
python rombestilling-ntnu.py
```

Legg inn brukernavn og pass i filen "login.cfg" med innholdet:
```bash
[section1]
user = test1
pass = test2
```
Filbanen til denne filen spesifiseres i skriptet.


TODO:

- [x] Brukernavn og passord i egen fil
- [x] Legge in lettere valg av rom
- [x] Legge inn automatisk tid 2 uker frem i tid
- [ ] Skjekk om rommet er ledig, og hvis ikke, velg annet rom
