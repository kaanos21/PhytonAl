import difflib
import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")  

komutlar = {
    "merhaba": "Selam! Size nasıl yardımcı olabilirim?",
    "hava nasıl": "Bugün hava güzel görünüyor (ama dışarı bakmak daha iyi olabilir :) ).",
    "nasılsın": "Ben bir yapay zeka ajanıyım, stabilim :)",
    "ne yapıyorsun": "Size yardımcı olmak için buradayım.",
    "görüşürüz": "Görüşmek üzere!",
    "çıkış": "Kapatılıyor..."
}

def komutu_bul(girdi):
    secenekler = list(komutlar.keys())
    en_benzer = difflib.get_close_matches(girdi.lower(), secenekler, n=1, cutoff=0.5)
    return en_benzer[0] if en_benzer else None

def llm_ile_cevapla(girdi):
    try:
        yanit = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kısa ve yardımcı cevaplar ver."},
                {"role": "user", "content": girdi}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return yanit.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM hatası]: {str(e)}"

def cevapla(girdi):
    if not girdi.strip():
        return "Bir şey yazmalısın."

    eslesen_komut = komutu_bul(girdi)
    if eslesen_komut:
        return komutlar[eslesen_komut]
    else:
        return llm_ile_cevapla(girdi)

def baslat():
    print("Yapay Zeka Ajanı başlatıldı. ('çıkış' yazarak çıkabilirsin.)\n")
    while True:
        girdi = input("Sen: ")
        if "çıkış" in girdi.lower():
            print("Ajan: Görüşmek üzere!")
            break
        yanit = cevapla(girdi)
        print("Ajan:", yanit)

if __name__ == "__main__":
    baslat()
