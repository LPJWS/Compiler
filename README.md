# Compiler
Исходный код для курсовой работы по дисциплине Прикладные Алгоритмы студента группы ИСБ-118 Волкова Даниила
## Запуск

Python-скрипт *main.py* ищет в директории файл input.code для считывания кода и выдаёт на выходе файл *output.ll* с байт-кодом для LLVM

### Библиотеки

*rply* - позволяет генерировать лексические и синтаксические анализаторы.

*llvmlite*  - генерирует байт-код для llvm

### Грамматика языка
КС-грамматика языка представлена ниже.

*main : program*

*program : statement_full*

*program : statement_full program'*

*statement_full : IF ( expression ) { block }*

*statement_full : IF ( expression ) { block } ELSE { block }*

*statement_full : WHILE ( expression ) { block }*

*statement_full : statement ;*
        
*block : statement_full*

*block : statement_full block*

*statement : expression*

*statement : BREAK*

*statement : CONTINUE*

*statement : PRINT ( expression )*

*statement : INT IDENTIFIER = expression*

*statement : FLT IDENTIFIER = expression*

*statement : IDENTIFIER = expression*

*expression : expression SUM expression*

*expression : expression SUB expression*

*expression : expression MUL expression*

*expression : expression DIV expression*

*expression : expression != expression*

*expression : expression == expression*

*expression : expression >= expression*

*expression : expression <= expression*

*expression : expression > expression*

*expression : expression < expression*

*expression : expression AND expression*

*expression : expression OR expression*

*expression : NOT expression*

*expression : SUMI ( expression , expression )*

*expression : SUMF ( expression , expression )*

*expression : SUBI ( expression , expression )*

*expression : SUBF ( expression , expression )*

*expression : IDENTIFIER*

*expression : const*

*expression : ( expression )*

*const : FLOAT*

*const : INTEGER*

*const : STRING*

Пример программы на созданном языке:

```
int a = 15;
int b = 10;

while (a != b){
        if (a > b) {
            a = sub(a, b);
        }
        else {
            b = sub(b, a);
        }
} 
print(a);
```

### Пример дерева разбора

[Imgur](https://imgur.com/KjetyiX)
