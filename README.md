# minecraft_telegram_online_bot
🌟unucu Takip Botu 🌟
Topluluğumuz için özel olarak geliştirilen bu Telegram botu, Minecraft sunucumuzun anlık durumunu kesintisiz olarak takip eder ve tüm bilgileri canlı olarak grubumuza yansıtır. Artık sunucunun durumunu merak etmenize gerek kalmayacak!

Botumuz Neler Yapar?
🔹 7/24 Otomatik Takip: Bot, siz komut vermeden, çalıştığı sürece her 20 saniyede bir sunucuyu kontrol eder.

🔹 Canlı Durum Paneli: Grupta sabit duran üç ana mesaj üzerinden tüm bilgileri anlık olarak günceller:

Anlık Durum: Sunucudaki oyuncu sayısını, o gün kırılan oyuncu rekorunu ve tüm zamanların rekorunu canlı olarak gösterir.

Açılış Kayıtları: Sunucunun son 5 açılış zamanını listeler.

Kapanış Kayıtları: Sunucunun son 5 kapanış zamanını listeler.

🔹 Akıllı Bildirimler:

Sunucu kapandığında gruba anında kalıcı bir bildirim gönderir.

Sunucu tekrar açıldığında, önceki kapanma bildirimini siler ve 30 saniye sonra kendini imha eden geçici bir "Sunucu Aktif!" mesajı yollar. Bu sayede sohbet kirliliği önlenir.

🔹 Kalıcı Hafıza: Bot yeniden başlasa veya mesajlar silinse bile, kaldığı yerden devam eder ve paneli otomatik olarak yeniden oluşturur.

🔹 Kolay Yönetim: Tüm ayarlar (config.json) ve botun mesajları (messages.json) ayrı dosyalarda tutulduğu için, gelecekte bot üzerinde değişiklik yapmak son derece kolaydır.

Nasıl Kurulur? (Kısa Rehber)
Botu çalıştırmak için aşağıdaki adımları izlemeniz yeterlidir:

Python Yükleyin: Bilgisayarınızda Python'un son sürümünün kurulu olduğundan emin olun.

Kütüphaneleri İndirin: Komut satırına pip install "python-telegram-bot[job-queue]" mcstatus yazarak gerekli kütüphaneleri yükleyin.

Ayarları Yapılandırın: config.json dosyasını açın ve içindeki TELEGRAM_TOKEN, TARGET_CHAT_ID gibi alanları kendi bilgilerinizle doldurun.

Çalıştırın: minecraft_bot.py dosyasını python minecraft_bot.py komutuyla çalıştırın.

Hepsi bu kadar! Botunuz artık sunucunuzu sizin için izlemeye hazır.
