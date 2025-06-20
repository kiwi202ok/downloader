import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import yt_dlp

BOT_TOKEN = "7394261933:AAFpJ31t6byHcmaBGVnTUtxA_v4ulFX-LL4"  # ← bu yerga o'z bot tokeningizni yozing

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎬 Xush kelibsiz!\n"
        "Menga YouTube, TikTok yoki Instagram havolasini yuboring.\n"
        "Men qanday bo‘lsa ham sizga videoni yuboraman ✅"
    )

@dp.message(F.text)
async def download_video(message: Message):
    url = message.text.strip()

    # 1. Faqat kerakli havolalarni tekshiramiz
    if not any(x in url for x in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com"]):
        return await message.answer("❗ Faqat YouTube, TikTok yoki Instagram havolasini yuboring.")

    await message.answer("⏬ Video yuklanmoqda, kuting...")

    filename = "video.mp4"

    # 2. Past sifat bilan yuklash (odatda 360p telegram uchun yetarli)
    ydl_opts = {
        "format": "best[height<=360][ext=mp4]/best[ext=mp4]/best",
        "outtmpl": filename,
        "quiet": True,
        "merge_output_format": "mp4"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Video")
            filesize = info.get("filesize") or info.get("filesize_approx") or 0

        # 3. Video fayl sifatida yuborish (50 MB dan kichik bo‘lsa)
        file = FSInputFile(filename)

        if os.path.getsize(filename) < 49 * 1024 * 1024:
            await message.answer_video(file, caption=f"🎥 {title}\n\n@yourbotdan yuklab olindi✅")
        else:
            # 4. Agar video katta bo‘lsa — hujjat sifatida yuboramiz (max 2GB)
            await message.answer_document(file, caption=f"📄 {title}\n\n@yourbotdan yuklab olindi✅")

        os.remove(filename)

    except Exception as e:
        # 5. Agar video Telegram limitidan oshsa — to‘g‘ridan-to‘g‘ri yuklab olish havolasini beramiz
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                direct_url = info.get("url")
                title = info.get("title", "Video")

            if direct_url:
                await message.answer(f"🚨 Fayl hajmi katta.\n\n📥 [{title}]({direct_url}) yuklab oling.",
                                     parse_mode="Markdown")
            else:
                await message.answer("❌ Videoni yuklab bo‘lmadi.")

        except Exception as err:
            await message.answer(f"❌ Xatolik: {err}")

async def main():
    print("🚀 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
