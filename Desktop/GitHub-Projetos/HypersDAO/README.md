# 🤖 HypersDAO Telegram Bot

Bot automático para monitoramento da HypersDAO com relatórios em tempo real via Telegram.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Funcionalidades

- 📊 Preço, market cap e volume em tempo real
- ⏰ Relatórios automáticos agendados (09:00, 12:00, 18:00, 21:00)
- 📈 Análise de tendências e métricas
- 🖼 Envio de relatórios com imagem
- 🔔 Comandos personalizados no Telegram

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7+
- Token do BotFather do Telegram
- Chat ID do Telegram

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/devdavidejesus/hypersdao-telegram-bot.git
cd hypersdao-telegram-bot

2. Instale as dependências:
```bash
pip install -r requirements.txt

3. Configure o bot:
cp config.example.py config.py
# Edite o config.py com suas credenciais

4. Execute o bot:
python HypersDAO.py

📋 Comandos Disponíveis
Comando	Descrição
/start	Menu inicial e boas-vindas
/price	Preço atual e variação
/marketcap	Market cap e liquidez
/volume	Volume e transações
/report	Relatório completo
🛠 Tecnologias Utilizadas
Python 3.13 - Linguagem principal

python-telegram-bot - API do Telegram

DexScreener API - Dados em tempo real

Requests - Requisições HTTP

Schedule - Agendamento de tarefas

⚠️ Importante
Nunca commit o arquivo config.py com tokens reais

Use config.example.py como template

Adicione config.py no .gitignore

👨‍💻 Desenvolvido por
Davi de Jesus

GitHub: @devdavidejesus
