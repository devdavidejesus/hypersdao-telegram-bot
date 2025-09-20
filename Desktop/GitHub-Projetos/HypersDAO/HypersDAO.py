"""
HYPERSDAO TELEGRAM BOT - by devdavidejesus
Bot automático com comandos para HypersDAO
GitHub: https://github.com/devdavidejesus

⚠️ CONFIGURAÇÃO NECESSÁRIA:
1. Crie um arquivo config.py com:
   BOT_TOKEN = "seu_token_do_botfather"
   CHAT_ID = "seu_chat_id_do_telegram" 
   LOGO_PATH = "caminho/para/imagem/hypersdao.jpg"

2. Instale as dependências: pip install -r requirements.txt
"""

import requests
import asyncio
import telegram
from datetime import datetime
import time
import schedule
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import os
import threading
import logging

# Configurações fixas
CONTRACT_ADDRESS = "7XiycwkFwd1ig3yhncPxaq3qwJ6S2RpHc63C541hgmdC"

# Configurações sensíveis
try:
    from config import BOT_TOKEN, CHAT_ID, LOGO_PATH
except ImportError:
    raise ImportError(
        "❌ Arquivo config.py não encontrado!\n"
        "👉 Crie um arquivo config.py com:\n"
        "BOT_TOKEN = 'seu_token_do_botfather'\n" 
        "CHAT_ID = 'seu_chat_id_do_telegram'\n"
        "LOGO_PATH = 'caminho/para/imagem/hypersdao.jpg'"
    )

# Logger configurado
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class HypersDAOTelegramBot:
    def __init__(self, contract_address, bot_token, chat_id):
        self.contract_address = contract_address
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = "https://api.dexscreener.com/latest/dex/tokens/"
        self.historical_data = []
        self.logo_path = LOGO_PATH

    # ============ API ============ #
    async def get_hypersdao_data(self):
        """Busca dados da HypersDAO"""
        try:
            response = requests.get(f"{self.base_url}{self.contract_address}", timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro na API: {e}")
            return None

    def extract_metrics(self, data):
        """Extrai métricas importantes"""
        if not data or "pairs" not in data or not data["pairs"]:
            return None

        pair = data["pairs"][0]

        metrics = {
            "timestamp": datetime.now(),
            "price_usd": float(pair.get("priceUsd", 0)),
            "volume_24h": float(pair.get("volume", {}).get("h24", 0)),
            "liquidity_usd": float(pair.get("liquidity", {}).get("usd", 0)),
            "market_cap": float(pair.get("marketCap", 0)),
            "price_change_24h": float(pair.get("priceChange", {}).get("h24", 0)),
            "price_change_1h": float(pair.get("priceChange", {}).get("h1", 0)),
            "buys_24h": pair.get("txns", {}).get("h24", {}).get("buys", 0),
            "sells_24h": pair.get("txns", {}).get("h24", {}).get("sells", 0),
        }
        metrics["txns_24h"] = metrics["buys_24h"] + metrics["sells_24h"]
        metrics["buy_sell_ratio"] = (
            metrics["buys_24h"] / metrics["sells_24h"]
            if metrics["sells_24h"] > 0 else 0
        )

        self.historical_data.append(metrics)
        return metrics

    # ============ Envio ============ #
    async def send_with_image(self, message, chat_id=None):
        """Envia mensagem com imagem da HypersDAO"""
        chat_id = chat_id or self.chat_id
        bot = telegram.Bot(token=self.bot_token)

        try:
            if os.path.exists(self.logo_path):
                with open(self.logo_path, "rb") as photo:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=photo,
                        caption="🚀 **HypersDAO Monitor** 🚀",
                        parse_mode=ParseMode.MARKDOWN
                    )

            await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
            logger.info("Mensagem enviada com sucesso ✅")
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {e}")

    # ============ Relatórios ============ #
    @staticmethod
    def _usd(val, digits=2):
        return f"${val:,.{digits}f}"

    def generate_price_report(self, m):
        return (
            "💰 **Preço HypersDAO**\n\n"
            f"💵 **Atual:** {self._usd(m['price_usd'], 8)}\n"
            f"📈 **24h:** {m['price_change_24h']:+.2f}%\n"
            f"⏰ **1h:** {m['price_change_1h']:+.2f}%\n"
            f"{'📈 Tendência: ALTA 🟢' if m['price_change_24h'] > 0 else '📉 Tendência: BAIXA 🔴'}\n"
            f"🕒 {datetime.now():%H:%M %d/%m}"
        )

    def generate_marketcap_report(self, m):
        return (
            "🎯 **Market Cap HypersDAO**\n\n"
            f"📊 Market Cap: {self._usd(m['market_cap'],0)}\n"
            f"🏊 Liquidez: {self._usd(m['liquidity_usd'],0)}\n"
            f"📈 Volume 24h: {self._usd(m['volume_24h'],0)}"
        )

    def generate_volume_report(self, m):
        return (
            "📊 **Volume HypersDAO**\n\n"
            f"💸 Volume 24h: {self._usd(m['volume_24h'],0)}\n"
            f"🔄 Transações: {m['txns_24h']:,}\n"
            f"✅ Compras: {m['buys_24h']:,}\n"
            f"❌ Vendas: {m['sells_24h']:,}"
        )

    def generate_full_report(self, m):
        tendencia = (
            "🔥 Tendência: FORTE ALTA" if m["price_change_24h"] > 10 else
            "📈 Tendência: ALTA" if m["price_change_24h"] > 0 else
            "📉 Tendência: BAIXA"
        )
        return (
            "🚀 **RELATÓRIO COMPLETO HYPERSDAO** 🚀\n\n"
            f"💰 Preço: {self._usd(m['price_usd'], 8)}\n"
            f"📈 Var 24h: {m['price_change_24h']:+.2f}%\n"
            f"🎯 Market Cap: {self._usd(m['market_cap'],0)}\n"
            f"🏊 Liquidez: {self._usd(m['liquidity_usd'],0)}\n"
            f"📊 Volume 24h: {self._usd(m['volume_24h'],0)}\n"
            f"🔄 Transações: {m['txns_24h']:,}\n"
            f"{tendencia}\n"
            f"🕒 {datetime.now():%d/%m/%Y %H:%M}"
        )

    # ============ Comandos ============ #
    async def _handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, generator):
        data = await self.get_hypersdao_data()
        if data:
            metrics = self.extract_metrics(data)
            if metrics:
                report = generator(metrics)
                await update.message.reply_text(report, parse_mode=ParseMode.MARKDOWN)

    async def price_command(self, update, context):
        await self._handle_command(update, context, self.generate_price_report)

    async def marketcap_command(self, update, context):
        await self._handle_command(update, context, self.generate_marketcap_report)

    async def volume_command(self, update, context):
        await self._handle_command(update, context, self.generate_volume_report)

    async def report_command(self, update, context):
        data = await self.get_hypersdao_data()
        if data:
            m = self.extract_metrics(data)
            if m:
                report = self.generate_full_report(m)
                await self.send_with_image(report, update.message.chat_id)

    async def start_command(self, update, context):
        welcome = f"""
🤖 **HypersDAO Monitor Bot** 🚀

Bem-vindo! Este bot fornece informações em tempo real sobre a HypersDAO.

📋 **Comandos disponíveis:**
/price - Preço atual e variação
/marketcap - Market Cap e liquidez  
/volume - Volume e transações
/report - Relatório completo

⏰ Relatórios automáticos: 09:00, 12:00, 18:00, 21:00
🔗 Contrato: {self.contract_address}
"""
        await self.send_with_image(welcome, update.message.chat_id)

    # ============ Agendador ============ #
    async def daily_report(self):
        logger.info("Gerando relatório automático...")
        data = await self.get_hypersdao_data()
        if data:
            m = self.extract_metrics(data)
            if m:
                await self.send_with_image(self.generate_full_report(m))

    def run_scheduler(self):
        def scheduler_loop():
            for hour in ["09:00", "12:00", "18:00", "21:00"]:
                schedule.every().day.at(hour).do(lambda: asyncio.run(self.daily_report()))
            logger.info("⏰ Agendador iniciado! Relatórios automáticos ativos")
            while True:
                schedule.run_pending()
                time.sleep(60)

        threading.Thread(target=scheduler_loop, daemon=True).start()

    # ============ Inicialização ============ #
    def setup_commands(self):
        app = Application.builder().token(self.bot_token).build()
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("price", self.price_command))
        app.add_handler(CommandHandler("marketcap", self.marketcap_command))
        app.add_handler(CommandHandler("volume", self.volume_command))
        app.add_handler(CommandHandler("report", self.report_command))
        return app


def main():
    bot = HypersDAOTelegramBot(CONTRACT_ADDRESS, BOT_TOKEN, CHAT_ID)
    app = bot.setup_commands()
    bot.run_scheduler()

    logger.info("🤖 Bot iniciado! Aguardando comandos...")
    app.run_polling()


if __name__ == "__main__":
    main()