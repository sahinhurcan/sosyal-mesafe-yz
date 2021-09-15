import utils.social_distanceing_config as config
from utils.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import imutils
import cv2
import os

# YOLO modelimizin eğitildiği COCO sınıfı etiketlerinin yüklenmesi
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
labels = open(labelsPath).read().strip().split("\n")

# YOLO ağırlıklarına ve model konfigürasyonuna giden yolları türetme
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# GPU kullanıp kullanmayacağının kontrolü
if config.USE_GPU:
    # target ve backend cuda konfigurasyonları
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPerferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# YOLO'dan ihtiyacımız olan *output* katmanlarının belirlenmesi
ln = net.getLayerNames()
ln = [ln[i[0] - 1 ] for i in net.getUnconnectedOutLayers()]

# video erişiminin sağlanması
print("Videoya erişiliyor")
vs = cv2.VideoCapture("video.mp4")
writer = None

while True:
    # frame'in okunması
    des, frame = vs.read()

    if not des:
        break

    # frame boyutlandırması ve tespiti
    frame = imutils.resize(frame, width=700)
    results = detect_people(frame, net, ln, personIdx=labels.index("person"))

    violate = set()

    # en az iki kişi olması kontrolü
    if len(results) >= 2:
        centroids = np.array([r[2] for r in results])
        D = dist.cdist(centroids, centroids, metric="euclidean")

        for i in range(0, D.shape[0]):
            for j in range(i + 1, D.shape[1]):

                if D[i, j] < config.MIN_DISTANCE:
                    violate.add(i)
                    violate.add(j)

    # lsonuç döngüsü
    for (i, (prob, bbox, centroid)) in enumerate(results):

        # kutu ve merkez kordinat ayarları
        (startX, startY, endX, endY) = bbox
        (cX, cY) = centroid
        color = (0, 255, 0)

        # mesafe ihlalini renklendirme
        if i in violate:
            color = (0, 0, 255)

        # sonuç verileri için ekran ayarlaması
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        cv2.circle(frame, (cX, cY), 5, color, 1)

    # toplam ihlal sayısının ekrana yazılması
    text = "Social Distance Violations: {}".format(len(violate))
    cv2.putText(frame, text, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

    cv2.imshow("Output", frame)

    # q ya basılması durumunda döngüden çıkılması
    key = cv2.waitKey(1) & 0xff
    if key == ord("q"):
        break

    # çıktının yazılması
    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter("output.avi", fourcc, 25, (frame.shape[1], frame.shape[0]), True)

    if writer is not None:
        writer.write(frame)



























