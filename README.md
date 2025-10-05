# minecraft_telegram_online_bot
🌟Sunucu Takip Botu 🌟
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

Botu sıfırdan kurup çalıştırmak için aşağıdaki adımları dikkatlice takip edin.

1. Gerekli Programların Kurulumu

Python: Bilgisayarınızda Python yüklü değilse, python.org adresinden indirin. Kurulum sırasında "Add Python to PATH" kutucuğunu işaretlediğinizden emin olun.

Kütüphaneler: Komut İstemi'ni (cmd) açıp pip install "python-telegram-bot[job-queue]" mcstatus komutunu çalıştırın.

2. Telegram Bot'unu Oluşturma

Telegram'da @BotFather'ı bulun ve /newbot komutuyla yeni bir bot oluşturun.

BotFather'ın size vereceği API Token'ını kopyalayın. Bu token'ı bir sonraki adımda kullanacağız.

3. Dosyaları Hazırlama

Bilgisayarınızda bot için bir klasör oluşturun.

Size verilen config.json, messages.json ve minecraft_bot.py dosyalarını bu klasörün içine koyun.

4. Grup ID'sini Alma (En Önemli Adım)

Grup Oluşturun: Botun çalışacağı bir Telegram grubu oluşturun veya mevcut bir grubu kullanın.

Botunuzu Gruba Ekleyin: Oluşturduğunuz botu (@kullaniciadi) bu gruba üye olarak ekleyin.

Botu Yönetici Yapın: Grup ayarlarından botunuzu yönetici yapın. Bu, mesajları düzenleyip silebilmesi için gereklidir.

ID Öğrenme: Grup ID'sini öğrenmek için, gruba geçici olarak @myidbot gibi bir ID botu ekleyin. Bot, gruba katıldığında sohbetin ID'sini (-100... ile başlayan bir sayı) mesaj olarak gönderecektir.

ID'yi Kopyalayın: Bu ID'yi kopyalayın ve sonrasında ID botunu gruptan çıkarabilirsiniz.

5. Ayarları Yapılandırma

Klasördeki config.json dosyasını bir metin düzenleyici ile açın.

TELEGRAM_TOKEN alanına BotFather'dan aldığınız token'ı yapıştırın.

TARGET_CHAT_ID alanına bir önceki adımda öğrendiğiniz grup ID'sini yapıştırın.

Dosyayı kaydedin.

6. Botu Çalıştırma

Komut İstemi'ni (cmd) açın ve cd komutuyla dosyaların olduğu klasöre gidin.

python minecraft_bot.py komutunu yazıp Enter'a basın.

Botunuz artık çalışmaya başlayacak ve 5 saniye içinde gruptaki paneli oluşturacaktır. Tebrikler!
