# SNAnalizer

### Przygotowanie książki


Plik z książką należy podzielić na rozdziały, można to zrobić uruchamiając: 
```sh
python tools/spliter.py book_path
```
w katalogu z książką powstanie nowy katalog o nazwie takiej jak plik z książką, w którym znajdować się będą pliki odpowiadające poszczególnym rozdziałom książki

Następnie należy dostarczyć listę bohaterów książki w pliku characters.txt utworzonym wyżej katalogu. Można też to zrobić automatycznie poprzez uruchomienie

```sh
python tools/generate_characters_list.py book_path
```