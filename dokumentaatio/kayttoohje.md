# Käyttöohje

Sovellusta on suoraviivaista käyttää komentoriviltä seuraavien komentojen avulla.

### Laskutoimituksen laskeminen

Sovelluksen käynnistyttyä voi heti antaa jonkin laskutoimituksen ja vastaus tulostuu komentoriville:
```shell
Command/expression: sin(pi/2)
= 1.0
```

### Funktion tallentaminen 

Anna ensin komento:
```shell
Command/expression: af
```
Anna seuraavaksi funktion nimi:
```shell
Enter the name of the function, i.e. 'f_1' -- 'exit' to cancel
name: f1
```
Lopuksi määrittele funktio esim:
```shell
Enter the function. I.e. 'x**2'
function: x**2
```
Nyt funktion arvon voi laskea seuraavasti:
```shell
Command/expression: f1(2)
= 4
```

### Muuttujan tallentaminen 

Anna ensin komento:
```shell
Command/expression: av
```
Anna seuraavaksi muuttujan nimi:
```shell
Enter the name of the variable: -- 'exit' to cancel
name: var
```
Lopuksi määrittele muuttuja esim:
```shell
Enter the variable. I.e. '2 + e^2 + f(5)'
variable: e^2
```
Nyt muuttujan arvoa voi käyttää seuraavasti:
```shell
Command/expression: var * 2
= 14.778112197861299
```

### Yhtälön ratkaisu

Anna ensin komento:
```shell
Command/expression: solve
```
Seuraavaksi anna yhtälö:
```shell
Enter the equation to solve. I.e. '2*x + 3 = 0'
equation: x^2 = 4
```
Komentoriville tulostuu lista ratkaisuista:
```shell
Solution: [-2, 2]
```
**(HUOM! Tällä hetkellä omien funktioiden käyttäminen ei ole mahdollista yhtälöissä)**

### Funktioiden ja muuttujien listaaminen
Komennoilla 'functions' tai 'variables' saa tulostettua listat käytettävissä olevista funktiosta ja muuttujista:
```shell
Command/expression: functions

   abs(x): abs(x)
   sqrt(x): math.sqrt(x)
   exp(x): math.exp(x)
   sin(x): math.sin(x)
   cos(x): math.cos(x)
   f1(x): x**2
```

```shell
Command/expression: variables

   e: math.e
   pi: math.pi
   var: e**2
```

### 
