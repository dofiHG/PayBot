from aiogram import Bot, Dispatcher, executor, types
import cfg
from aiogram.types import ContentType

bot = Bot(cfg.token)
dp = Dispatcher(bot)

price = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_invoice(message.chat.id,
                           title='Подписка на бота', 
                           description='Описание товара', 
                           provider_token=cfg.pay_token1,
                           currency='rub', 
                           prices=[price], 
                           is_flexible=False,
                           start_parameter='one-month-subscription',
                           payload='text-invoice-payload')
        
@dp.pre_checkout_query_handler(lambda querty: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def sucsessfull_payment(message: types.Message):
    print('SUCCESSFUL PAYMENT:')
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    print("***********************************************************************************")

    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошёл успешно!!!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)