from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message,FSInputFile,InputMediaPhoto
from menucommands.set_bot_commands import set_default_commands
from data import config
import asyncio
import logging
import sys
from baza.create import users_db
from baza.add_user import add as add_user
from filters.admin import IsBotAdminFilter
from keyboard_buttons import admin_keyboard
from baza.all_users import allusers,allusers_id
from aiogram.fsm.context import FSMContext #new
from states.reklama import Adverts
import time 
from filters.check_sub_channel import IsCheckSubChannels
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from insta_uz import insta_save
from my_youtube import youtube_save
from tiktok_uz import tiktok_save
ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        add_user(full_name=full_name,telegram_id=telegram_id)
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz")
    except:
        await message.answer(text="Assalomu alaykum")


@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message:Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = allusers()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = allusers_id()
    count = 0
    for user in users:
        try:
            bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.5)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()



@dp.message(F.text.contains("instagram"))
async def instagram_download(message:Message):
    link = message.text
    result = insta_save(link)
    if result[0]=="video":
        await message.answer_video(video=result[1],caption="Admin: @shuhratik_007")
    elif result[0]=="rasm":
        await message.answer_photo(photo=result[1], caption="Admin: @shuhratik_007")
    else:
        await message.answer("You sent the wrong link")


@dp.message(F.text.contains("youtu"))
async def youtube_download(message:Message):

    result = youtube_save(message.text)
    video = FSInputFile(result)
    await message.answer_video(video=video, caption="ADMIN: @shuhratik_007")


@dp.message(F.text.contains("tiktok"))
async def tiktok_download(message:Message):
    link = message.text
    tiktok = tiktok_save(link)
    video=tiktok.get("video")
    music=tiktok.get("music")
    rasmlar=tiktok.get("images")
    if rasmlar: 
        rasm = []
        for i,r in enumerate(rasmlar):
            rasm.append(InputMediaPhoto(media=r))
            if (i+1)%10==0:
                await message.answer_media_group(rasm)
                rasm=[]
        if rasm:
            await message.answer_media_group(rasm)
    elif video:
        await message.answer_video(video=video,caption="Admin: @shuhratik_007")
    if music: 
        await message.answer_audio(audio=music)



@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

#bot ishga tushganini xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    users_db() #database yaratildi
    await set_default_commands(bot)
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())