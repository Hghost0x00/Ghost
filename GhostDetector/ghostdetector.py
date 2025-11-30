import pydivert
import os
import time
from colorama import Fore
import threading

Telegram_API_IP = "149.154.167.220"

def telegram_recon():
    try:
        with pydivert.WinDivert("tcp.DstPort == 443") as w:
            print("Sniffer Started... Press Ctrl+C to stop.")
            
            for packet in w:
                w.send(packet)

                if packet.dst_addr == f"{Telegram_API_IP}":
                    print(Fore.YELLOW + "[Telegram API Detected]" + Fore.RESET)
    except KeyboardInterrupt:
        print(Fore.RED + "Exiting.." + Fore.RESET)
        os._exit(1)

def file_creation_analysis():
    def enumeration_txt(start_dir="C:\\", output="all_txt.txt"):
        with open(output, 'w', encoding="utf-8") as out:
            for root, dirs, files in os.walk(start_dir):
                for f in files:
                    if f.lower().endswith(".txt"):
                        out.write(os.path.join(root, f) + "\n")

        print(Fore.GREEN + f"Enumeration Done. Saved to {output}" + Fore.RESET)

    enumeration_txt()

    txt_files = []
    with open("all_txt.txt", 'r', encoding="utf-8") as f:
        txt_files = [line.strip() for line in f if line.strip()]

    file_sizes = {}
    for file in txt_files:
        if os.path.exists(file):
            try:
                file_sizes[file] = os.path.getsize(file)
            except:
                pass
    print(Fore.GREEN + "Monitoring files..." + Fore.RESET)

    while True:
        time.sleep(0.5)

        for file in list(file_sizes.keys()):
            current_size = os.path.getsize(file)

            if current_size != file_sizes[file]:
                print(f"File Modified: {file} -> {current_size}")
                file_sizes[file] = current_size

def main():
    print(Fore.CYAN + rf"""
  ________.__                    __ ________          __                 __                
 /  _____/|  |__   ____  _______/  |\______ \   _____/  |_  ____   _____/  |_  ___________ 
/   \  ___|  |  \ /  _ \/  ___/\   __\    |  \_/ __ \   __\/ __ \_/ ___\   __\/  _ \_  __ \
\    \_\  \   Y  (  <_> )___ \  |  | |    `   \  ___/|  | \  ___/\  \___|  | (  <_> )  | \/
 \______  /___|  /\____/____  > |__|/_______  /\___  >__|  \___  >\___  >__|  \____/|__|   
        \/     \/           \/              \/     \/          \/     \/                   

made by @hghost010 - https://github.com/Hghost0x00
""")
    
    print(Fore.YELLOW + """
[1] Start Telegram Detection
[2] Start File Creation Analysis
[3] Start Both

[0] Exit
""")
    
    try:
        choice = input(Fore.CYAN + "Enter your choice: " + Fore.RESET)
    except KeyboardInterrupt:
        print(Fore.RED + "\nExiting..." + Fore.RESET)
        os._exit(0)

    if choice == "1":
        print(Fore.GREEN + "Starting the telegram recon module..." + Fore.RESET)
        telegram_recon()
    elif choice == "2":
        print(Fore.GREEN + "Starting the file creation analysis module..." + Fore.RESET)
        file_creation_analysis()
    elif choice == "3":
        print(Fore.GREEN + "Starting GhostDetector..." + Fore.RESET)

        telegram_thread = threading.Thread(target=telegram_recon, daemon=True)
        file_thread = threading.Thread(target=file_creation_analysis, daemon=True)

        telegram_thread.start()
        file_thread.start()

        try:
            telegram_thread.join()
            file_thread.join()
        except KeyboardInterrupt:
            print(Fore.RED + "Exiting..")
            os._exit(0)

    elif choice == "0":
        print(Fore.RED + "Exiting.." + Fore.RESET)
        os._exit(0)

if __name__ == "__main__":
    main()
