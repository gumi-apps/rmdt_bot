"""
This is Freshman Tricks Bot
Developer @nurads
"""

import time, re, os
from django.conf import settings
from telebot import TeleBot

from .models import Contact, Management
from .messages import *
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ChatJoinRequest,
)

start_msg = start_msg.replace("Remedial", "Freshman")
about_us_msg = about_us_msg_bot2

bot = TeleBot(settings.BOT_TOKEN2, parse_mode="HTML", threaded=False)

bot_number = 2
contact_us_msg = fr_contact_us
tg_channel_url_natural = "https://t.me/AUTExamChannel"
tg_channel_url_social = "https://t.me/+8MTwQ16Xx5FmNWJk"
tg_channel_url_AUTexam = "https://t.me/+8MTwQ16Xx5FmNWJk"

# tg_channel_id_natural = -1002419752883
# tg_channel_id_social = -1002462494621
bot_name = "Freshman Tricks Bot"
pricing = 1000

channels = {
    # "class a": {"link": "https://t.me/+Qbqk4EH8QVk3OWNk", "id": -1002419752883},
    "class a": {"link": "https://t.me/+xup8moOjHQBjNzFk", "id": -1002727288430},
    "Freshman class for 2018": {
        "link": "https://t.me/+xup8moOjHQBjNzFk",
        "id": -1002727288430,
    },
    # ... other classes ...
    "UAT Exam": {"link": " https://t.me/+H1xihl9rt8w4MTJk", "id": -1003077513192},
    "class b": {"link": "https://t.me/+8MTwQ16Xx5FmNWJk", "id": -1002462494621},
    "class c": {"link": "https://t.me/+JuEqcFOCJno2MDc0", "id": -1002473698743},
    "class d": {"link": "https://t.me/+0ryxUqkw2GpmOWJk", "id": -1002384868135},
}


def get_payment_options():
    reply = InlineKeyboardMarkup()

    # Existing payment options
    reply.add(InlineKeyboardButton("🟢ቴሌ ብር ", callback_data="_payment_tb"))
    reply.add(InlineKeyboardButton("🟢የኢትዮጵያ ንግድ ባንክ", callback_data="_payment_cbe"))
    reply.add(InlineKeyboardButton("🟢ዳሸን ባንክ", callback_data="_payment_dsh"))
    reply.add(InlineKeyboardButton("🟢አማራ ባንክ", callback_data="_payment_am"))
    reply.add(
        InlineKeyboardButton("🟢ኦሮሚያ international ባንክ", callback_data="_payment_oib")
    )
    reply.add(InlineKeyboardButton("🟢አቢሲኒያ ባንክ", callback_data="_payment_ab"))
    reply.add(InlineKeyboardButton("🟢አባይ ባንክ", callback_data="_payment_aba"))
    reply.add(InlineKeyboardButton("🟢አዋሽ ባንክ", callback_data="_payment_aw"))
    reply.add(InlineKeyboardButton("🟢ኮፕሬቲቭ ባንክ", callback_data="_payment_coop"))

    return reply


def get_keyboard(**kwargs):
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=kwargs.get("one_time_keyboard") is not None,
    )

    if not kwargs:
        keyboard.add(
            KeyboardButton("📝 Register"),
            KeyboardButton("About Us"),
            KeyboardButton("Contact Us"),
        )
    else:
        ls = []
        for key, value in kwargs.items():
            ls.append(KeyboardButton(" ".join(key.split("_")), **value))
        keyboard.add(*ls)
    return keyboard


def get_inline_keyboard(**kwargs):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key, value in kwargs.items():
        buttons.append(
            InlineKeyboardButton(value, callback_data=key),
        )

    return markup.add(*buttons)


@bot.message_handler(commands=["start", "restart"])
@bot.message_handler(func=lambda msg: msg.text.lower() in ["start", "restart"])
def start_hadler(message):
    tg_user = message.from_user
    welcome_text = start_msg  # or a custom greeting
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=get_keyboard(),  # show main menu buttons
    )


@bot.message_handler(func=lambda msg: msg.text.lower() == "help")
@bot.message_handler(commands=["help"])
def help_handler(message):
    bot.send_message(message.chat.id, help_msg)


@bot.message_handler(commands=["aboutus"])
@bot.message_handler(func=lambda msg: msg.text.lower() == "about us")
def about_handler(message):
    bot.send_message(message.chat.id, about_us_msg)


@bot.message_handler(commands=["contactus"])
@bot.message_handler(func=lambda msg: msg.text.lower() == "contact us")
def contactus_handler(message):
    bot.send_message(message.chat.id, contact_us_msg)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    con = message.contact

    data = {
        "tg_id": message.from_user.id,
        "chat_id": message.chat.id,
        "bot_number": bot_number,
    }
    print(con)

    contact, iscreated = Contact.objects.get_or_create(**data)
    contact.first_name = con.first_name
    contact.last_name = con.last_name
    contact.phone_number = con.phone_number
    contact.username = message.from_user.username
    contact.save()

    if iscreated:
        msg1 = bot.send_message(
            message.chat.id, "Contact Received✅", reply_markup=get_keyboard()
        )
    else:
        msg1 = bot.send_message(
            message.chat.id, "Contact Updated Succeslly✅", reply_markup=get_keyboard()
        )

    time.sleep(0.5)

    bot.delete_message(message.chat.id, msg1.id)
    reg_handler(message)


def receipt_upload_handler(message: Message):
    print(message.photo)
    print(message.document)
    doc = message.document
    img = message.photo
    if img is None and doc is None:
        bot.register_next_step_handler(message, receipt_upload_handler)
        bot.send_message(
            message.chat.id,
            "Upload only photos",
            reply_markup=get_inline_keyboard(cancel="cancel"),
        )
        return

    if img:
        file_id = img[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        send_to_admin(message, downloaded_file)
    if doc and doc.mime_type in ["image/jpeg", "image/jpg", "image/png", "image/bmp"]:
        file_id = doc.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        send_to_admin(message, downloaded_file)

    con = Contact.objects.filter(
        tg_id=message.from_user.id, bot_number=bot_number
    ).first()

    if not con:
        bot.send_message(message.chat.id, "Share your Contact")
        return
    msg = f"""Join Channel below
{channels[con.selected_class]['link']}
    
<b>NB. It will be approved if the receipt is valid</b>
    """

    bot.send_message(message.chat.id, msg, reply_markup=get_keyboard())
    # if con.stream == "natural":
    #     bot.send_message(
    #         message.chat.id,
    #         tg_channel_url_natural,
    #         reply_markup=get_keyboard(),
    #     )
    # else:
    #     bot.send_message(
    #         message.chat.id,
    #         tg_channel_url_social,
    #         reply_markup=get_keyboard(),
    #     )


@bot.message_handler(commands=["register"])
@bot.message_handler(func=lambda msg: msg.text == "📝 Register")
def reg_handler(message, grade=None, stream=None):
    mgt = Management.getInstance()

    bot.delete_message(message.chat.id, message.id)
    if not mgt.registration_open:
        bot.send_message(message.chat.id, "Registration is closed🚫 contact the admin")
        return
    con = Contact.objects.filter(
        tg_id=message.from_user.id, bot_number=bot_number
    ).first()
    if not con:
        mark = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        mark.add(KeyboardButton("Share Contact", request_contact=True))
        bot.send_message(
            message.chat.id, "Share Contact to Register", reply_markup=mark
        )

        return
    if con.reg_completed:
        bot.send_message(
            message.chat.id, "Already Registered🚫", reply_markup=get_keyboard()
        )
        return
    # bot.send_message(
    #     message.chat.id,
    #     "What stream are you in?",
    #     reply_markup=get_inline_keyboard(
    #         _natural="Natural",
    #         _social="Social",
    #         # _class_c="Class C",
    #         # _class_d="Class D",
    #     ).add(
    #         InlineKeyboardButton("cancel", callback_data="cancel"),
    #     ),
    # )
    bot.send_message(
        message.chat.id,
        "What class you are registering for?",
        reply_markup=get_inline_keyboard(
            _class_a="Freshman class for 2018",
            _aut_exam="UAT Exam Registration",  # <-- new button
        ).add(
            InlineKeyboardButton("cancel", callback_data="cancel"),
        ),
    )


@bot.callback_query_handler(func=lambda call: call.data in ["_natural", "_social"])
def stream_call_back(call: CallbackQuery):
    con = Contact.objects.filter(tg_id=call.from_user.id, bot_number=bot_number).first()
    tg_user = call.from_user
    # TODO


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["_class_a", "_class_b", "_class_c", "_class_d", "_aut_exam"]
)
def class_call_back(call: CallbackQuery):
    con = Contact.objects.filter(tg_id=call.from_user.id, bot_number=bot_number).first()
    tg_user = call.from_user

    if call.data == "_class_a":
        con.stream = "Both Natural & Social"
        con.selected_class = "Freshman class for 2018"
        required_payment = 1000
        grade_text = "Freshman(2018)"
        con.amount_to_pay = 1000  # Set the default price

    elif call.data == "_class_b":
        con.stream = "Natural"
        con.selected_class = "Class B"
        required_payment = 1000
        grade_text = "Class B"
    elif call.data == "_class_c":
        con.stream = "Social"
        con.selected_class = "Class C"
        required_payment = 1000
        grade_text = "Class C"
    elif call.data == "_class_d":
        con.stream = "Both"
        con.selected_class = "Class D"
        required_payment = 1000
        grade_text = "Class D"
    elif call.data == "_aut_exam":
        con.stream = "UAT Exam"
        con.selected_class = "UAT Exam"
        required_payment = 300
        grade_text = "UAT Exam"
        # con.amount_to_pay = 300  # Set the new price

    con.save()
    bot.delete_message(call.message.chat.id, call.message.id)

    msg = f"""
<b>Confirm Your Registration</b>
-----------------------------------
Name: {tg_user.first_name}
Grade: {grade_text}
Stream: {con.stream}
Required Payment: {required_payment} ETB
"""
    bot.send_message(
        call.message.chat.id,
        msg,
        reply_markup=get_inline_keyboard(reg_confirm="Confirm").add(
            InlineKeyboardButton("back", callback_data="_edit_stream"),
            InlineKeyboardButton("cancel", callback_data="cancel"),
        ),
    )


# def class_call_back(call: CallbackQuery):
#     con = Contact.objects.filter(tg_id=call.from_user.id, bot_number=bot_number).first()
#     tg_user = call.from_user

#     if call.data == "_aut_exam":
#         con.selected_class = "UAT Exam"
#         con.stream = "N/A"
#         price = 300  # UAT Exam payment
#     else:
#         con.selected_class = call.data.replace("_", " ").strip()
#         con.stream = "Both Natural & Social"
#         price = pricing  # Freshman fee


#     con.stream = "Both Natural & Social"
#     con.selected_class = call.data.replace("_", " ").strip()
#     con.save()
#     bot.delete_message(call.message.chat.id, call.message.id)
#     msg = f"""
#         <b>Confirm Your Registration</b>
#         -----------------------------------
#         Name: {tg_user.first_name}
#         Grade: {grade_text}
#         Stream: {con.stream},
#         Required Payment: {pricing} ETB
#         """
#     bot.send_message(
#         call.message.chat.id,
#         msg,
#         reply_markup=get_inline_keyboard(reg_confirm="Confirm").add(
#             InlineKeyboardButton("back", callback_data="_edit_stream"),
#             InlineKeyboardButton("cancel", callback_data="cancel"),
#         ),
#     )


@bot.callback_query_handler(func=lambda call: call.data == "_edit_stream")
def back_to_stream(call):
    return reg_handler(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data in ["reg_confirm", "_back_payment"]
)
def reg_confirm(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == "reg_confirm":
        tg_user = call.from_user
        con = Contact.objects.filter(tg_id=tg_user.id, bot_number=bot_number).first()

        con.save()

        pr = 300 if con.selected_class == "UAT Exam" else pricing

        bot.send_message(
            call.message.chat.id,
            f"🌸የክፍያ አማራጮች🌸\n\nPlease select a payment option to proceed with the registration. Pay amount of {pr} ETB",
            # "🌸የክፍያ አማራጮች🌸|Payment Options",
            reply_markup=get_payment_options(),
        )


@bot.callback_query_handler(func=lambda call: re.match(r"_payment_*", call.data))
def selected_payment_option_call_back(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    con = Contact.objects.filter(tg_id=call.from_user.id, bot_number=bot_number).first()
    amount_to_show = 300 if con.selected_class == "UAT Exam" else pricing

    data = {
        "_payment_tb": {
            "msg": "🟢ቴሌ ብር",
            "acc": "0927052140",
        },
        "_payment_cbe": {
            "msg": "🟢የኢትዮጵያ ንግድ ባንክ",
            "acc": "1000390400668",
        },
        "_payment_dsh": {
            "msg": "🟢ዳሸን ባንክ",
            "acc": "5325387344011",
        },
        "_payment_am": {
            "msg": "🟢አማራ ባንክ",
            "acc": "9900008823565",
        },
        "_payment_oib": {
            "msg": "🟢ኦሮሚያ international ባንክ =6047345",
            "acc": "6047345",
        },
        "_payment_ab": {
            "msg": "🟢አቢሲኒያ ባንክ",
            "acc": "157584488",
        },
        "_payment_aba": {
            "msg": "🟢አባይ ባንክ",
            "acc": "1349011003253717",
        },
        "_payment_aw": {
            "msg": "🟢አዋሽ ባንክ",
            "acc": "013351173115900",
        },
        "_payment_coop": {
            "msg": "🟢ኮፕሬቲቭ ባንክ",
            "acc": "1000400219994",
        },
    }

    msg = f"""
    {data[call.data]["msg"]}
    
    Name: Yared Getachew Teshome
    Account: {data[call.data]["acc"]}
    amount: {amount_to_show} ETB
    ------------------
    Upload Receipt After Payment.
    
    Please click upload receipt before sending a file
    """

    bot.send_message(
        call.message.chat.id,
        msg,
        reply_markup=get_inline_keyboard(
            _back_payment="back", _upload_receipt="Upload Receipt"
        ),
    )


@bot.callback_query_handler(func=lambda call: call.data == "_upload_receipt")
def upload_receipt(call):
    bot.clear_step_handler(call.message)
    bot.send_message(call.message.chat.id, "Upload photo of the receipt")
    bot.register_next_step_handler(call.message, receipt_upload_handler)


@bot.callback_query_handler(func=lambda msg: msg.data == "cancel")
def cancel(call):
    bot.clear_step_handler(call.message)
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.chat_join_request_handler(func=lambda msg: True)
def auto_approve_chat_join_request(request: ChatJoinRequest):
    print("Approving automatically!!!", request.chat.id)
    tg_user = request.from_user
    con = Contact.objects.filter(tg_id=tg_user.id, bot_number=bot_number).first()
    if con:
        if (
            not con.join_approved
            or channels[con.selected_class]["id"] != request.chat.id
        ):
            return
        bot.approve_chat_join_request(request.chat.id, request.from_user.id)
        # bot.approve_chat_join_request(channels[con.selected_class])
        # if con.stream == "natural" and tg_channel_id_natural == request.chat.id:
        # elif tg_channel_id_social == request.chat.id:
        #     bot.approve_chat_join_request(tg_channel_id_social, request.from_user.id)


@bot.callback_query_handler(
    func=lambda call: re.match("_approve_chat_-?\\d+_user_-?\\d+", call.data)
)
def approve_chat_join(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.id)
    try:
        data = call.data.split("_")
        user_id = int(data[-1])
        chat_id = int(data[3])
        con = Contact.objects.filter(tg_id=user_id, bot_number=bot_number).first()
        con.join_approved = True
        con.reg_completed = True
        con.save()
        bot.approve_chat_join_request(chat_id, user_id)
        msg = bot.send_message(call.message.chat.id, "Approved✅")
        time.sleep(2)
        bot.delete_message(call.message.chat.id, msg.id)
    except Exception as e:
        msg1 = bot.send_message(
            call.message.chat.id,
            "Will be approved by the bot automatically when requested👍",
        )
        print(e)
        msg = bot.send_message(call.message.chat.id, str(e))
        time.sleep(2)
        bot.delete_message(call.message.chat.id, msg.id)
        bot.delete_message(call.message.chat.id, msg1.id)


@bot.callback_query_handler(
    func=lambda call: re.match("_decline_chat_-?\\d+_user_-?\\d+", call.data)
)
def decline_chat_join(call: CallbackQuery):
    data = call.data.split("_")
    user_id = int(data[-1])
    chat_id = int(data[3])
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.decline_chat_join_request(chat_id, user_id)
        msg = bot.send_message(call.message.chat.id, "Declined🚫")
        time.sleep(1)
        bot.delete_message(call.message.chat.id, msg.id)
    except Exception as e:
        pass


def send_to_admin(message, photo: bytes):
    contact = Contact.objects.filter(
        tg_id=message.from_user.id, bot_number=bot_number
    ).first()
    admins = Contact.objects.filter(is_admin=True, bot_number=bot_number)
    channel_id = channels[contact.selected_class]["id"]
    for admin in admins:
        bot.send_photo(
            admin.chat_id,
            photo,
            reply_markup=get_inline_keyboard(
                **{
                    f"_approve_chat_{channel_id}_user_{message.from_user.id}": "Approve",
                    f"_decline_chat_{channel_id}_user_{message.from_user.id}": "Decline",
                }
            ),
            caption=f"""
            You are Receiving this message from {bot_name} because you are an admin
            User: {contact.first_name} {contact.last_name if contact.last_name is not None else ''}
            username: {contact.username}
            Phone: {contact.phone_number}
            Grade: {contact.grade}
            Class: {contact.selected_class.capitalize()}
            """,
        )
