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

# Minecraft Sunucu Botu Kurulum Rehberi 


Bu rehber, Minecraft sunucunuzun durumunu takip eden gelişmiş Telegram botunu, tüm özellikleriyle nasıl kuracağınızı ve çalıştıracağınızı en baştan sona kadar anlatır.

Adım 1: Gerekli Programların Kurulumu
Python: Bilgisayarınızda Python yüklü değilse, python.org adresinden en son sürümü indirin. Kurulum sırasında ekranın en altında çıkan "Add Python to PATH" kutucuğunu mutlaka işaretleyin.

Gerekli Kütüphaneler: Bilgisayarınızda Komut İstemi'ni (cmd) veya Terminal'i açın ve aşağıdaki komutu yapıştırıp Enter'a basarak gerekli Python eklentilerini kurun:

pip install "python-telegram-bot[job-queue]" mcstatus

Adım 2: Telegram Bot'u Oluşturma
Telegram'da @BotFather'ı aratıp sohbete başlayın.

Yeni bir bot oluşturmak için /newbot komutunu gönderin.

Botunuz için bir isim ve ardından _bot ile biten bir kullanıcı adı belirleyin.

BotFather'ın size vereceği API Token'ını kopyalayın. Bu token'ı bir sonraki adımda kullanacağız.

Adım 3: Dosyaları Hazırlama
Bilgisayarınızda bot için yeni bir klasör oluşturun.

Size verilen minecraft_bot.py, config.json ve messages.json dosyalarının üçünü de bu klasörün içine koyun.

Adım 4: Grup ID'sini Alma ve Ayarları Yapma
Bu en önemli adımdır. Botun hangi gruba mesaj atacağını bu adımla belirleyeceğiz.

Grup Oluşturun: Botun çalışacağı bir Telegram grubu oluşturun veya mevcut bir grubu kullanın.

Botu Gruba Ekleyin: Oluşturduğunuz botu (@kullanici_adi) bu gruba üye olarak ekleyin.

Botu Yönetici Yapın: Grup ayarlarından botunuzu yönetici yapın. Bu, mesajları düzenleyip silebilmesi için gereklidir.

Token'ı Girin: Klasörünüzdeki config.json dosyasını bir metin editörü (Not Defteri gibi) ile açın. BURAYA_TOKENINIZI_GIRIN yazan yere 2. Adım'da aldığınız API Token'ını yapıştırın. Dosyayı kaydedin. TARGET_CHAT_ID şimdilik 0 kalabilir.

Botu Geçici Olarak Çalıştırın: Komut İstemi'ni açın ve cd komutuyla dosyaların olduğu klasöre gidin. Ardından python minecraft_bot.py komutuyla botu çalıştırın.

ID'yi Öğrenin: Bot çalışırken, onu eklediğiniz gruba gidin ve sohbete /idogren komutunu yazın. Bot, size sohbetin ID'sini (-100... ile başlayan bir sayı) mesaj olarak gönderecektir. Bu ID'yi kopyalayın.

Botu Durdurun: Komut İstemi ekranında klavyeden CTRL ve C tuşlarına aynı anda basarak botu durdurun.

Ayarları Tamamlayın: config.json dosyasını tekrar açın. TARGET_CHAT_ID alanına bir önceki adımda kopyaladığınız grup ID'sini yapıştırın. Sunucu IP ve isim ayarlarını da kontrol edip dosyayı son kez kaydedin.

Adım 5: Bot'u Kalıcı Olarak Çalıştırma
Komut İstemi'ne geri dönün.

Aşağıdaki komutu çalıştırarak botu başlatın:

python minecraft_bot.py

Botunuz artık doğru grupta çalışmaya başlayacak ve 5 saniye içinde durum panelini oluşturacaktır. Tebrikler!

Önemli Not: Bot, sadece Komut İstemi/Terminal penceresi açık olduğu sürece çalışır. Pencereyi kapatırsanız bot durur.
