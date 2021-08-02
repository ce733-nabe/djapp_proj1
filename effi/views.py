from django.shortcuts import render, redirect
import base64

import os
import sys
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import tensorflow as tf
import time

from .models import Image

model = tf.keras.applications.EfficientNetB2(weights='imagenet')

def effi_pred(file_name):
    img = image.load_img(file_name, target_size=(260, 260))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    x = tf.constant(x)

    y = model.predict(x,steps=1)
    print(decode_predictions(y))
    return y

def upload(request):  
    
    #画像データの取得
    files = request.FILES.getlist("files[]")
 
    #簡易エラーチェック（jpg拡張子）
    for memory_file in files:
        root, ext = os.path.splitext(memory_file.name)
        if ext != '.jpg':
            message ='【ERROR】jpg以外の拡張子ファイルが指定されています。'
            return render(request, 'effi/index.html', {'message': message})
 
    if request.method =='POST' and files:
        result=[]
        labels=[]
        for file in files:
            labels.append(effi_pred(file))
        
        for file, label in zip(files, labels):
            file.seek(0)
            file_name = file
            src = base64.b64encode(file.read())
            src = str(src)[2:-1]
            result.append((src, label))
            
        return render(request, 'effi/result.html', {'result': result})
    
    else:
        return redirect('index')
        
def showall(request):
    images = Image.objects.all()
    context = {'images':images}
    return render(request, 'album/showall.html', context)