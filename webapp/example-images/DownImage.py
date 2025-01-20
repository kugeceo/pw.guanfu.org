import os
import cv2
import requests
from tqdm import tqdm

imageUrls = [
    'http://unsplash.com/photos/FHvpa4-Fpu8/download?ixid=MnwxMjA3fDB8MXxzZWFyY2h8MjZ8fGNvdXBsZXxlbnwwfHx8fDE2NTY1ODkzNTc&force=true&w=2400',
    'http://unsplash.com/photos/h2pnXHMz8YM/download?ixid=MnwxMjA3fDB8MXxzZWFyY2h8NDV8fHdvbWVufGVufDB8fHx8MTY1NjU4Nzg4MQ&force=true&w=1920',
    'http://unsplash.com/photos/j9pRzpabS94/download?ixid=MnwxMjA3fDB8MXxzZWFyY2h8MTUwfHxoYW5kfGVufDB8fHx8MTY1NjY2OTk1MA&force=true&w=1920',
    'http://unsplash.com/photos/7_TTPznVIQI/download?force=true&w=1920',
    "http://images.unsplash.com/photo-1496857239036-1fb137683000?ixlib=rb-1.2.1&dl=ivan-jevtic-p7mo8-CG5Gs-unsplash.jpg&w=2400&q=80&fm=jpg&crop=entropy&cs=tinysrgb",
]
fixSize = 4096


def DownFile(url: str, savefile: str):
    r = requests.get(url)
    with open(savefile, 'wb') as fp:
        fp.write(r.content)


def GeneratePreview(sfile: str, dfile: str,  preSize=(64, 64)):
    srcImage = cv2.imread(sfile, cv2.IMREAD_COLOR)
    shortSize = min(srcImage.shape[0:2])
    rowStart = int((srcImage.shape[0] - shortSize) / 2)
    rowEnd = rowStart + shortSize
    colStart = int((srcImage.shape[1] - shortSize) / 2)
    colEnd = colStart + shortSize
    roi = srcImage[rowStart: rowEnd, colStart: colEnd]
    if shortSize > fixSize:
        roi = cv2.resize(roi, (fixSize, fixSize), interpolation=cv2.INTER_AREA)
        shortSize = fixSize

    img = cv2.resize(roi, preSize, interpolation=cv2.INTER_AREA)
    cv2.imwrite(dfile, img)


Path = os.path.abspath(os.path.dirname(__file__))
for inx, imgUrl in enumerate(tqdm(imageUrls)):
    savePath = os.path.join(Path, str(inx + 1) + '.jpg')
    savePath_preview = os.path.join(Path, str(inx + 1) + '_preview' + '.jpg')
    DownFile(imgUrl, savePath)
    GeneratePreview(savePath, savePath_preview)
