# Testautomation med CI - Individuell Inlämning - TESTANALYS

## Vad ska testas? - Inledande undersökning
https://tetrifact.manafeed.com/
En sida där man kan ladda upp och lagra paket, samt ladda ned dem.
Sidan är skriven i JS. Det finns även API, men jag ska testa UI:et.
Sidan är skriven av min man, det är en demosida för hans projekt Tetrifact, 
därför har jag även tillgång till källkoden: https://github.com/shukriadams/tetrifact

- Göra en kort exploratory testing av sidan för att bekanta mig med den för att avgöra vad som är lämpligt att testa.
- Ladda hem och titta på källkoden.

## Varför testar vi?
Testuppdraget är speciellt, eftersom det sker inom ramen för en skolkurs, men om det var skarpt läge
skulle jag säga att jag vill säkerställa att det inte finns uppenbara buggar. Det är inte en väldigt
avancerad sida, den har begränsad användning. Vi vet inte vem användaren är, men kan anta att det är någon
med relativt god teknisk kunskap. Vi behöver inte testa användarvänlighet, vi ska testa funktion, det är viktiga.
därför att hemsidan är ett tekniskt hjälpmedel, ett redskap. Vi skulle ev. kunna ge råd om kvalitet och hur
effektiviteten kan ökas, om vi märker av förbättringsområden.

## SFDIPOT

Från SFDIPOT har jag sållit ut nedanstående, vilket jag anser är applicerbart på min produkt.

### Function - Everything that the product does. 

- Calculation: any arithmetic function or arithmetic operations embedded in other functions. 
- Time-related: time-out settings; periodic events; time zones; business holidays; terms and warranty periods; chronograph functions.
- Error Handling: any functions that detect and recover from errors, including all error messages.
- Interactions: any interactions between functions within the product. 

### Data - Everything that the product processes. 
- Input/Output: any data that is processed by the product, and any data that results from that processing. 
- Preset: any data that is supplied as part of the product, or otherwise built into it, such as prefabricated databases, default values, etc. 
- Persistent: any data that is expected to persist over multiple operations. This includes modes or states of the product, such as options settings, 
view modes, contents of documents, etc.
- Interdependent/Interacting: any data that influences or is influenced by the state of other data; or jointly influences an output.
- Sequences/Combinations: any ordering or permutation of data, e.g. word order, sorted vs. unsorted data, order of tests.
- Cardinality: numbers of objects or fields may vary (e.g. zero, one, many, max, open limit). Some may have to be unique (e.g. database keys).
- Big/Little: variations in the size and aggregation of data. 
- Invalid/Noise: any data or state that is invalid, corrupted, or produced in an uncontrolled or incorrect fashion.

### Time?
Testerna ska gå snabbt att köra, dvs lägga aldrig in Wait eller Tidsargument.//JP, pres 4 (Testpyramiden), sida 16.
