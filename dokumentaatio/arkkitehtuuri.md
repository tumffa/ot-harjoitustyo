```mermaid
 classDiagram
    ServiceHandler "1" -- "1" ConsoleIO
    ServiceHandler "1" -- "1" Translator
    Translator ..> ConsoleIO
```
