checks whether look-alike characters are actually the same string or not. It also checks for invisible characters that form hidden messages. Credits for this latter mechanism go to paulgb

## how I personally compiled it
```
mkdir ~/my_binary
cd ~/my_binary
python -m venv venv
source venv/bin/activate  
pip install pyinstaller pyqt5
pip install --upgrade pip
venv/bin/pyinstaller --onefile ~/my_binary/Symbol_Checker_v2/symbol_checker_v2.py      
```


## test emoji with hidden message:
😂󠅔󠅟󠄐󠅩󠅟󠅥󠄐󠅣󠅕󠅕󠄐󠅤󠅘󠅙󠅣󠄐󠅣󠅥󠅠󠅕󠅢󠄐󠅣󠅕󠅓󠅢󠅕󠅤󠄐󠅝󠅕󠅣󠅣󠅑󠅗󠅕󠄯󠄐󠄹󠄐󠅔󠅟󠅞󠄗󠅤󠄞
