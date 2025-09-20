# 🤖 HypersDAO Telegram Bot

Bot automático para monitoramento da HypersDAO com relatórios em tempo real

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Telegram API](https://img.shields.io/badge/telegram-bot%20API-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Last Commit](https://img.shields.io/github/last-commit/devdavidejesus/hypersdao-telegram-bot)
![Repo Size](https://img.shields.io/github/repo-size/devdavidejesus/hypersdao-telegram-bot)

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

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! 

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🐛 Reportando Bugs

Se encontrar algum bug, por favor abra uma [issue](https://github.com/devdavidejesus/hypersdao-telegram-bot/issues) no GitHub.
