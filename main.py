from TikTokPy import TikTokPy
from fake_useragent import UserAgent
import time
import random

# Fungsi untuk mendapatkan user-agent acak
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Fungsi untuk memasukkan dan memverifikasi cookie
def get_cookie():
    print("=== Masukkan Cookie TikTok Anda ===")
    cookie = input("Tempelkan cookie TikTok Anda di sini: ").strip()

    if not cookie:
        print("Cookie tidak valid. Harap tempelkan cookie yang benar.")
        exit()
    return cookie

# Proxy untuk menyamarkan IP
proxy = "http://username:password@proxy_address:port"  # Ganti dengan proxy Anda
use_proxy = input("Apakah Anda ingin menggunakan proxy? (y/n): ").strip().lower()
proxies = {"http": proxy, "https": proxy} if use_proxy == "y" else None

# Memilih mode auto follow
mode_paksa = input("Apakah Anda ingin menggunakan mode paksa sampai 300 followers? (y/n): ").strip().lower()

# Fungsi auto follow
async def auto_follow(cookie):
    # Set user-agent awal
    current_user_agent = get_random_user_agent()

    async with TikTokPy(
        custom_cookie=cookie,
        proxies=proxies,  # Proxy (opsional)
        headers={"User-Agent": current_user_agent},  # User-Agent awal
    ) as bot:
        target_username = input("Masukkan username target yang followers-nya ingin di-follow: ").strip()
        followers = await bot.get_user_followers(target_username)

        # Tetapkan jumlah maksimum aksi
        max_followers = 300 if mode_paksa == "y" else random.randint(30, 50)
        print(f"Target follow hari ini: {max_followers} followers.")

        action_count = 0
        follow_count = 0  # Counter untuk rotasi user-agent

        for follower in followers:
            if action_count >= max_followers:
                print("Target tercapai. Berhenti.")
                break

            try:
                # Follow user
                await bot.follow(follower)
                print(f"Followed: {follower}")
                action_count += 1
                follow_count += 1

                # Rotasi user-agent setiap 5 kali follow
                if follow_count >= 5:
                    current_user_agent = get_random_user_agent()
                    bot.headers.update({"User-Agent": current_user_agent})
                    print(f"User-Agent diubah: {current_user_agent}")
                    follow_count = 0  # Reset counter

                # Jeda acak untuk setiap tindakan
                time.sleep(random.randint(60, 180))
            except Exception as e:
                print(f"Error: {e}")
                continue

        # Jika mode paksa aktif dan belum mencapai target 300, ulangi
        while mode_paksa == "y" and action_count < 300:
            print("Mengambil lebih banyak followers...")
            followers = await bot.get_user_followers(target_username)  # Ambil daftar baru
            for follower in followers:
                if action_count >= 300:
                    print("Berhasil mencapai 300 followers. Berhenti.")
                    break

                try:
                    await bot.follow(follower)
                    print(f"Followed: {follower}")
                    action_count += 1
                    follow_count += 1

                    # Rotasi user-agent setiap 5 kali follow
                    if follow_count >= 5:
                        current_user_agent = get_random_user_agent()
                        bot.headers.update({"User-Agent": current_user_agent})
                        print(f"User-Agent diubah: {current_user_agent}")
                        follow_count = 0  # Reset counter

                    time.sleep(random.randint(60, 180))
                except Exception as e:
                    print(f"Error: {e}")
                    continue

# Jalankan script
if __name__ == "__main__":
    # Baca cookie dari input
    cookie = get_cookie()

    # Jalankan auto follow
    import asyncio
    asyncio.run(auto_follow(cookie))
