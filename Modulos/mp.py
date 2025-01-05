python
import requests
import uuid
import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configurações do token de acesso e do bot
ACCESS_TOKEN = "APP_USR-3725334823147849-112610-ccb72a76edc39a5c0902ac0975e8c553-2069289633"
TELEGRAM_TOKEN = "7835190128:AAEyl7RKHfuQRdOu6KvjU0XHEnxiYqTwppI"

# Função para gerar UUID v4
def generate_uuid_v4():
    return str(uuid.uuid4())

# Função para criar um pagamento
def create_payment():
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Idempotency-Key": generate_uuid_v4()
    }
    data = {
        "transaction_amount": 1,
        "description": "PAGAR COM PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "felopesdosantos@gmail.com",
            "first_name": "Fernanda",
            "last_name": "Lopes",
            "identification": {
                "type": "CPF",
                "number": "191191191-00"
            }
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.text}")
        return None

# Função para verificar o status do pagamento
def verify_payment_status(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        getPay = response.json()
        status = getPay["status"]
        if status == "approved":
            return "\nPAGAMENTO APROVADO"
        elif status == "pending":
            return "\nESPERANDO PAGAMENTO"
        elif status == "cancelled":
            return "\nPAGAMENTO CANCELADO"
    else:
        print(f"Erro: {response.text}")
        return "ERRO"

# Função do bot para iniciar o pagamento
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Use o comando /pagar para iniciar um pagamento.')

def pagar(update: Update, context: CallbackContext) -> None:
    payment_data = create_payment()
    if payment_data:
        qr_code = payment_data['point_of_interaction']['transaction_data']['qr_code']
        payment_id = payment_data['id']
        update.message.reply_text(f"Use este código PIX para pagar: {qr_code}")
        
        while True:
            status = verify_payment_status(payment_id)
            update.message.reply_text(status)
            if status == "\nPAGAMENTO APROVADO" or status == "\nPAGAMENTO CANCELADO":
                break
            time.sleep(300)
    else:
        update.message.reply_text("Erro ao criar pagamento.")

# Função principal para iniciar o bot
def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pagar", pagar))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()