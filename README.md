# Sosyal Mesafe Algılama

## Amaç: Yayaların sosyal mesafeyi koruyup korumadığını tespit etmek
## Proje İşleyişi :

1. Web kamerasından veya video dosyasından video girişi.
2. Yayaları tespit etmek için önceden eğitilmiş bir yolov3 modeli kullanımı.
3. Yolov3 modelinin çıktısından yayaların ağırlık merkezini ölçümü.
4. Piksel değerlerinin mesafeyle eşlenmesi.
5. Merkez kordinat arası mesafe ölçümü.
6. Mesafeyi aşan kişilerin renklendirilmesi.
7. Çıktıyla birlikte mesafeyi aşan kişii sayısının gösterimi.

## proje çıktısının videosu için [tıklayın](https://youtu.be/V42a2mVDeuY)

### kaynak olarak www.pyimagesearch.com sitesindeki blog yazılarından faydalanılmıştır.