# 🪙 AliExpress Coin Collector

Automação em PyQt5 para coletar moedas na página de recompensas do AliExpress Mobile.

## 📦 Requisitos

- Python 3.8+
- pip

## 🛠️ Instalação

```bash
git clone https://github.com/CassGabriel/AliCoinGabriel.git
cd aliexpress-coin-collector
pip install -r requirements.txt
```

## 🚀 Executando

```
py aliexpress_mobile.py
```

## 📦 Gerar Executável (build)
```
pip install pyinstaller
pyinstaller --onefile --noconsole --windowed aliexpress_mobile.py
```

O executável será gerado na pasta dist/.