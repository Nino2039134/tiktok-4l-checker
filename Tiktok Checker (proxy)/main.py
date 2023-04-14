echo "# tiktok-4l-checker" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Nino2039134/tiktok-4l-checker.git
git push -u origin main

try:
    import requests, ctypes, time, os, threading, platform, json, random
    from colorama import Fore
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")

ascii_text = """
 .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. |
| |     ____     | || |   _____      | || |  _________   | |
| |   .'    `.   | || |  |_   _|     | || | |_   ___  |  | |
| |  /  .--.  \  | || |    | |       | || |   | |_  \_|  | |
| |  | |    | |  | || |    | |   _   | || |   |  _|  _   | |
| |  \  `--'  /  | || |   _| |__/ |  | || |  _| |___/ |  | |
| |   `.____.'   | || |  |________|  | || | |_________|  | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------' 
  """


if platform.system() == "Windows":
    clear = "cls"
else:
    clear = "clear"

class tiktok:

    def __init__(self):
        self.lock = threading.Lock()
        self.checking = True
        self.usernames = []
        self.unavailable = 0
        self.available = 0
        self.counter = 0

    def update_title(self):
        remaining = len(self.usernames) - (self.available + self.unavailable)
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"TikTok Username Checker | Available: {self.available} | Unavailable: {self.unavailable} | Checked: {(self.available + self.unavailable)} | Remaining: {remaining} | Developed by mr big dick luc"
        )
    
    def safe_print(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()
    
    def print_console(self, status, arg, color = Fore.RED):
        self.safe_print(f"       {Fore.WHITE}[{color}{status}{Fore.WHITE}] {arg}")
    
    def check_username(self, username):
        if username.isdigit():
            self.unavailable += 1
            self.print_console("Unavailable", username)
            return
        with requests.Session() as session:
            try:
                with open("proxy_list1.txt", "r") as f:
                    proxy_list1 = [proxy.strip() for proxy in f.readlines()]

                if not proxy_list1:
                    # If the file is empty, fetch new proxies and save them to the file
                    raise FileNotFoundError
            except FileNotFoundError:
                proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all"
                proxy_response = requests.get(proxy_url)
                proxy_list1 = [proxy for proxy in proxy_response.text.strip().split("\r\n") if not proxy.startswith("https://")]

            with open("proxy_list1.txt", "w") as f:
                for proxy in proxy_list1:
                    f.write(proxy + "\n")

            # Choose a random proxy from the list
            proxy = {"http": random.choice(proxy_list1)}
            
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US",
                "content-type": "application/json"
            }
            r = session.head("https://www.tiktok.com/@{}".format(username), headers=headers, proxies=proxy)
            if r.status_code == 200:
                self.unavailable += 1
                self.print_console("Unavailable", username)
            elif r.status_code == 404:
                self.available += 1
                self.print_console("Available or Banned", username, Fore.GREEN)
                requests.post("https://discord.com/api/webhooks/1096424221816664135/hY3kNZapSOOiZVoJT1atY13P76rlBArDWzYi_EeG_WKq6HbLEAhVvLMdk1fgJcs9X5zQ", json={"content": f"{username} available/banned @everyone claim"})

            self.update_title()
 
    def load_usernames(self):
        if not os.path.exists("usernames.txt"):
            self.print_console("Console", "File usernames.txt not found")
            time.sleep(10)
            os._exit(0)
        with open("usernames.txt", "r", encoding = "UTF-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                self.usernames.append(line)
            if not len(self.usernames):
                self.print_console("Console", "No usernames loaded in usernames.txt")
                time.sleep(10)
                os._exit(0)

    
    def main(self):
        os.system(clear)
        if clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW("TikTok Username Checker | Developed by mr big dick luc on Github")
        print(Fore.RED + ascii_text)
        self.load_usernames()
        threads = int(input(f"       {Fore.WHITE}[{Fore.RED}Console{Fore.WHITE}] Threads: "))
        print()
        if threads >= 5: #To prevent ratelimits
            threads = 5
        
        def thread_starter():
            self.check_username(self.usernames[self.counter])
        while self.checking:
            if threading.active_count() <= threads:
                try:
                    threading.Thread(target = thread_starter).start()
                    self.counter += 1
                except:
                    pass
                if len(self.usernames) <= self.counter:
                    self.checking = None
