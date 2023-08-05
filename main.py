import telebot
import requests
import time
from telebot import types
from config import *
import random
from text import *


bot = telebot.TeleBot(api_id)
keyboard = types.InlineKeyboardMarkup()
headers = {
    "Rocket-Pay-Key": api_key,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

balance_ago = requests.get(f"{endpoint}app/info", headers=headers).json()["data"]["balances"][19]["balance"]


game = open("num.txt", "r+")
game_number = game.read()
game.seek(0)
game.write(str(int(game_number) + 1))
game.close()


game_key = random.randint(1, 100000)
game_key_out = random.randint(1, 100)


def generate_transfer(tg_id, amount_t):
    data_t = {
        "tgUserId": tg_id,
        "currency": jetton,
        "amount": amount_t,
        "transferId": str(random.randint(1, 100000000000000000)),
        "description": f"KUBIKI by Rav — раунд #%s \nПобеда\n\nКлюч проверки: {game_key}" % game_number,
    }
    return data_t


data = {
    "minPayment": 1,
    "numPayments": 0,
    "currency": jetton,
    "description": f"Исход",
    "hiddenMessage": "Вы успешно поставили!\n\n"
                     f"{(game_key / game_key_out)}",
    "callbackUrl": "https://t.me/+-rQmUF7Pcb4zODRi",
    "expiredIn": bet_time + 5,
}

first_is_bigger = None
second_is_bigger = None
equal = None
sum_is_odd = None
sum_is_even = None
two_is_even = None
two_is_odd = None
bigger_than_45 = None
six_2 = None
no_equal = None


def main():
    global first_is_bigger, second_is_bigger, equal, sum_is_odd, sum_is_even, two_is_odd, two_is_even, bigger_than_45, \
        six_2, no_equal
    data["description"] = "KUBIKI — раунд #%s \nИсход 🎲 > 🎲" % game_number
    first_is_bigger = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход 🎲 < 🎲" % game_number
    second_is_bigger = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход 🎲 = 🎲" % game_number
    equal = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход сумма четная" % game_number
    sum_is_even = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход сумма нечетная" % game_number
    sum_is_odd = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход оба четные" % game_number
    two_is_even = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход оба нечетные" % game_number
    two_is_odd = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход сумма больше 4.5" % game_number
    bigger_than_45 = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход 6+6" % game_number
    six_2 = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    data["description"] = "KUBIKI — раунд #%s \nИсход 🎲 ≠ 🎲" % game_number
    no_equal = requests.post(f"{endpoint}tg-invoices", headers=headers, json=data).json()

    buttonFIB = types.InlineKeyboardButton(
        text=f"🎲 > 🎲 (X{one_is_bigger_coef})", url=first_is_bigger["data"]["link"]
    )
    keyboard.add(buttonFIB)
    buttonFIS = types.InlineKeyboardButton(
        text=f"🎲 < 🎲 (X{one_is_bigger_coef})", url=second_is_bigger["data"]["link"]
    )
    keyboard.add(buttonFIS)
    buttonNOB = types.InlineKeyboardButton(
        text=f"🎲 = 🎲 (X{equal_coef})", url=equal["data"]["link"]
    )
    keyboard.add(buttonNOB)
    button_noe = types.InlineKeyboardButton(
        text=f"🎲 ≠ 🎲 (X{no_equal_coef})", url=no_equal["data"]["link"]
    )
    keyboard.add(button_noe)
    buttonSNO = types.InlineKeyboardButton(
        text=f"Сумма чётная (X{sum_coef})", url=sum_is_even["data"]["link"]
    )
    keyboard.add(buttonSNO)
    buttonSIO = types.InlineKeyboardButton(
        text=f"Сумма нечётная (X{sum_coef})", url=sum_is_odd["data"]["link"]
    )
    keyboard.add(buttonSIO)
    buttonTIE = types.InlineKeyboardButton(
        text=f"Оба четные (X{two_is_coef})", url=two_is_even["data"]["link"]
    )
    keyboard.add(buttonTIE)
    buttonTIO = types.InlineKeyboardButton(
        text=f"Оба нечетные (X{two_is_coef})", url=two_is_odd["data"]["link"]
    )
    keyboard.add(buttonTIO)
    buttonBT45 = types.InlineKeyboardButton(
        text=f"Сумма больше 4.5 (X{bigger_than_45_coef})",
        url=bigger_than_45["data"]["link"],
    )
    keyboard.add(buttonBT45)
    buttonSIX = types.InlineKeyboardButton(
        text=f"6️⃣ + 6️⃣ (X{six_coef})", url=six_2["data"]["link"]
    )
    keyboard.add(buttonSIX)


main()

message = bot.send_message(
    chat_id,
    start.format(game_number, bet_time, max_payment),
    reply_markup=keyboard,
    parse_mode="html",
)
a = 0

while a < bet_time - 1:
    a += 15
    time.sleep(15)
    bot.edit_message_text(
        text=start.format(game_number, bet_time - a, max_payment),
        chat_id=chat_id,
        message_id=message.message_id,
        reply_markup=keyboard,
        parse_mode="html",
    )


bot.edit_message_text(
    text="Раунд #" + str(game_number) + "\n<b>Бросаем кубики...</b>",
    chat_id=chat_id,
    message_id=message.message_id,
    parse_mode="html",
)


def get_bet(out):
    pay = requests.get(
        f"{endpoint}tg-invoices/{out['data']['id']}", headers=headers, json=data
    ).json()["data"]["payments"]
    dictionary_local = {}
    if pay:
        for h in pay:
            user = h["userId"]
            amount = h["paymentAmount"]
            dictionary_local[user] = dictionary_local.get(user, 0) + amount
    return dictionary_local


dice1 = bot.send_dice(chat_id=chat_id)
dice2 = bot.send_dice(chat_id=chat_id)

fis_d = get_bet(first_is_bigger)
sim_d = get_bet(second_is_bigger)
nob_d = get_bet(equal)
sno_d = get_bet(sum_is_even)
sio_d = get_bet(sum_is_odd)
tie_d = get_bet(two_is_even)
tio_d = get_bet(two_is_odd)
b45_d = get_bet(bigger_than_45)
six_d = get_bet(six_2)
noe_d = get_bet(no_equal)

two_is = ""
result = ""
reward = 0
winners = 0
odd = ""
b_45 = ""
six = ""
no_equal_res = ""
bets = {}


def write_bet(dictionary):
    for n in dictionary.keys():
        bets[n] = bets.get(n, 0) + dictionary[n]


write_bet(six_d)
write_bet(sim_d)
write_bet(tie_d)
write_bet(fis_d)
write_bet(sio_d)
write_bet(b45_d)
write_bet(tio_d)
write_bet(sno_d)
write_bet(nob_d)
write_bet(noe_d)

winners_pool = {}
to_burn = 0


def get_winners(outcome, coef):
    global to_burn, winners_pool
    for r in outcome.keys():
        if outcome[r] <= max_payment:
            winners_pool[r] = winners_pool.get(r, 0) + outcome[r] * coef
        else:
            winners_pool[r] = winners_pool.get(r, 0) + max_payment * coef
            to_burn += float((outcome[r] - max_payment) * 0.80)


@bot.channel_post_handler(content_types=["dice"])
def handle_channel_dice():
    global reward, result, winners, odd, two_is, b_45, winners_pool, six, no_equal_res
    if dice1.dice.value > dice2.dice.value:
        result = f"🎲 > 🎲 (x{one_is_bigger_coef})"
        get_winners(fis_d, one_is_bigger_coef)

    if dice1.dice.value < dice2.dice.value:
        result = f"🎲 < 🎲 (x{one_is_bigger_coef})"
        get_winners(sim_d, one_is_bigger_coef)

    if dice1.dice.value == dice2.dice.value:
        result = f"🎲 = 🎲 (x{equal_coef})"
        get_winners(nob_d, equal_coef)

    if dice1.dice.value != dice2.dice.value:
        no_equal_res = f"🎲 ≠ 🎲 (x{no_equal_coef})\n"
        get_winners(noe_d, no_equal_coef)

    if ((dice1.dice.value + dice2.dice.value) % 2) == 0:
        odd = f"четная (x{sum_coef})"
        get_winners(sno_d, sum_coef)

    elif ((dice1.dice.value + dice2.dice.value) % 2) == 1:
        odd = f"нечетная (x{sum_coef})"
        get_winners(sio_d, sum_coef)

    if dice1.dice.value % 2 == 0 and dice2.dice.value % 2 == 0:
        two_is = f"\nОба четные (X{two_is_coef})"
        get_winners(tie_d, two_is_coef)

    if dice1.dice.value % 2 == 1 and dice2.dice.value % 2 == 1:
        two_is = f"\nОба нечетные (X{two_is_coef})"
        get_winners(tio_d, two_is_coef)

    if dice1.dice.value + dice2.dice.value > 4.5:
        b_45 = f"\nСумма больше 4.5 (X{bigger_than_45_coef})"
        get_winners(b45_d, bigger_than_45_coef)

    if dice1.dice.value == dice2.dice.value and dice2.dice.value == 6:
        six = f"\n6 + 6 (X{six_coef})"
        get_winners(six_d, six_coef)


handle_channel_dice()


if len(winners_pool.keys()) > 0:
    for winner in winners_pool.keys():
        winners += 1
        reward += winners_pool[winner]
        requests.post(
            f"{endpoint}app/transfer",
            headers=headers,
            json=generate_transfer(winner, winners_pool[winner]),
        )


bot.send_message(
    chat_id=chat_id,
    text=end.format(
        game_number,
        winners,
        reward,
        dice1.dice.value,
        dice2.dice.value,
        result,
        no_equal_res,
        odd,
        two_is,
        b_45,
        six,
    ),
)


balance = requests.get(f"{endpoint}app/info", headers=headers).json()["data"]["balances"][19]["balance"]

statistic = {}
for i in bets.keys():
    try:
        statistic[i] = float(bets[i]) - float(winners_pool[i])
    except KeyError:
        statistic[i] = float(bets[i])


res = ''
if balance - balance_ago > 0:
    res = '📈'
else:
    res = '📉'


bot.send_message(
    chat_id=adm,
    text=adm_text.format(game_number, game_key,
                         game_key_out, bets, winners_pool,
                         statistic, balance, balance - balance_ago, res),
)


burn_file = open("to_burn.txt", "r+")
to_burn_a = float(burn_file.read())
burn_file.seek(0)
burn_file.write(str(int(to_burn + to_burn_a)))
burn_file.close()
