import numpy as np
from numpy.ma.core import exp

views = 109693
reposts = 17
comms = 22
has_photo = 1
has_video = 0
intercept = 6.36
likes = 1142

y = intercept + 0.004 * comms + (-0.37) * has_photo + 0.36 * has_video + 1.05e-05 * views
print('y_log =', y)
print('y_pred =', np.expm1(y))
z = (np.log1p(likes) - np.log1p(np.expm1(y))) / 0.54
print('z =', z)
print(f'Пост переоценен/недооценен на {round((likes / np.expm1(y) - 1) * 100, 2)}%')

views = 104446
reposts = 133
comms = 293
has_photo = 0
has_video = 1
intercept = 6.36
likes = 10272

y = intercept + 0.004 * comms + (-0.37) * has_photo + 0.36 * has_video + 1.05e-05 * views
print('y_log =', y)
z = (np.log1p(likes) - np.log1p(np.expm1(y))) / 0.54
print('z =', z)
print(f'Пост переоценен/недооценен на {round((likes / np.expm1(y) - 1) * 100, 2)}%')