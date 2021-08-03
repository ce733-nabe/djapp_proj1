from django.shortcuts import render, redirect
from .models import Image
from .forms import ImageForm
from django.conf import settings

def showall(request):
    images = Image.objects.all()
    max_id = Image.objects.latest('id').id
    obj = Image.objects.get(id = max_id)
    
    file_name = str(settings.BASE_DIR) + str(obj.picture.url)
    print('file_name'.format(file_name))
    
    result = effi_pred(file_name)
    
    context = {'images':images, 'result':result}
    return render(request, 'album/showall.html', context)
    
def upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('album:showall')
    else:
        form = ImageForm()

    context = {'form':form}
    return render(request, 'album/upload.html', context)
   
   
from django.shortcuts import render, redirect
import base64

import os
import sys
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import tensorflow as tf
import time
import glob

def effi_pred(file):
    model = tf.keras.applications.EfficientNetB2(weights='imagenet')
    print('file:{}'.format(file))
    
    img = image.load_img(file, target_size=(260, 260))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    x = tf.constant(x)

    y = model.predict(x,steps=1)
    print(decode_predictions(y))

    return decode_predictions(y)
