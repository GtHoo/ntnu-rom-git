Dette skriptet er for å booke rom på ntnu (gjøvik) gjennom tp.uio.no 
Det kan hende det vil fungere på andre lokasjoner, men dette er ikke testet.

Kan bruke crontab for å kjøre denne etter midnatt da dette er tiden nye rom legges ut for 2 uker frem i tid.
```bash
crontab -e
```
Eksempelet under kjører dette hver torsdag of fredag og bokker dermed rom 2 uker frem i tid. og logger 
```bash
0 0 * * 4-5 /usr/bin/python /home/folder/rombestilling-ntnu.py > /home/folder/ntnurom.log
```

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
