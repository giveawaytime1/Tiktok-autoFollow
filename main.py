from TikTokPy import TikTokPy
from fake_useragent import UserAgent
import time
import random
import requests

# Fungsi untuk mendapatkan user-agent acak
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Fungsi untuk mendapatkan Access Token menggunakan OAuth 2.0
def get_access_token():
    print("=== Login ke Akun TikTok ===")
    # Gantilah URL ini dengan URL otorisasi dari TikTok
    authorization_url = "https://www.tiktok.com/auth/authorize/?client_key=<YOUR_CLIENT_KEY>&response_type=code&scope=user.info.basic&redirect_uri=<YOUR_REDIRECT_URI>"
    print(f"Klik URL berikut untuk login dan mendapatkan authorization code: {authorization_url}")
    
    authorization_code = input("Masukkan authorization code yang Anda terima: ").strip()

    # Menukar authorization code dengan access token
    url = 'https://open-api.tiktok.com/oauth/access_token/'
    data = {
        'client_key': '<YOUR_CLIENT_KEY>',
        'client_secret': '<YOUR_CLIENT_SECRET>',
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': '<YOUR_REDIRECT_URI>',
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token = response.json()['data']['access_token']
        print(f"Access token diperoleh: {access_token}")
        return access_token
    else:
        print("Error mendapatkan access token:", response.json())
        return None

# Proxy untuk menyamarkan IP
proxy = "http://username:password@proxy_address:port"  # Ganti dengan proxy Anda
use_proxy = input("Apakah Anda ingin menggunakan proxy? (y/n): ").strip().lower()
proxies = {"http": proxy, "https": proxy} if use_proxy == "y" else None

# Memilih mode auto follow
mode_paksa = input("Apakah Anda ingin menggunakan mode paksa sampai 300 followers? (y/n): ").strip().lower()

# Fungsi auto follow
async def auto_follow(access_token):
    # Set user-agent awal
    current_user_agent = get_random_user_agent()

    # Menggunakan TikTokPy dengan access token
    async with TikTokPy(access_token=access_token, proxies=proxies, headers={"User-Agent": current_user_agent}) as bot:
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
    # Dapatkan access token melalui OAuth 2.0
    access_token = get_access_token()
    if access_token:
        # Jalankan auto follow dengan access token
        import asyncio
        asyncio.run(auto_follow(access_token))
